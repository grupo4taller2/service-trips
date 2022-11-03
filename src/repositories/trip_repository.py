from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.database.requested_trip_dto import RequestedTripDTO
from src.database.taken_trip_dto import TakenTripDTO

from src.repositories.base_repository import BaseRepository
from src.service_layer.exceptions import TripNotFoundException
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import TripFacade
from src.domain.rider import Rider
from src.domain.directions import Directions
from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance

from src.utils.formatters import TimeFormatter, DistanceFormatter


class TripMapper:

    def trip_to_sql(self, trip: Trip):
        pass

    def sql_to_trip(self, sql_trip):
        rider: Rider = Rider(sql_trip.rider_username)
        origin: Location = Location(sql_trip.origin_address,
                                    sql_trip.origin_latitude,
                                    sql_trip.origin_longitude)

        destination: Location = Location(sql_trip.destination_address,
                                         sql_trip.destination_latitude,
                                         sql_trip.destination_longitude)

        time: Time = Time(sql_trip.estimated_time,
                          TimeFormatter().format(sql_trip.estimated_time))

        distance: Distance = Distance(
            sql_trip.distance,
            DistanceFormatter().format(sql_trip.distance))

        directions: Directions = Directions(origin,
                                            destination,
                                            time,
                                            distance)
        return Trip(
            id=UUID(sql_trip.id),
            rider=rider,
            directions=directions,
            type=sql_trip.type,
            state=TripFacade().create_from_name(sql_trip.state),
            estimated_price=sql_trip.estimated_price)


class TripRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def save(self, trip: Trip):
        trip_dto = RequestedTripDTO.from_entity(trip)
        self.session.add(trip_dto)

    def update(self, trip: Trip):
        raise NotImplementedError

    def find_by_id(self, id: str):
        try:
            trip_dto = self.session.query(RequestedTripDTO) \
                .filter_by(id=id).one()
        except NoResultFound:
            raise TripNotFoundException(id)
        except Exception as e:
            raise e

        # FIXME: Recuperar más datos si no es looking_for_driver
        trip = trip_dto.to_entity()
        self.seen.add(trip)
        return trip

    def find_for_driver_state_offset_limit(self,
                                           username: str,
                                           state: str,
                                           offset: int,
                                           limit: int):

        trip_dtos = self.session.query(RequestedTripDTO) \
            .filter_by(state=state)

        trip_dtos = trip_dtos.join(TakenTripDTO,
                                   TakenTripDTO.id == RequestedTripDTO.id,
                                   isouter=True)

        trip_dtos = trip_dtos.limit(limit).offset(offset)
        mapper = TripMapper()

        return [mapper.sql_to_trip(t_dto) for t_dto in trip_dtos]
