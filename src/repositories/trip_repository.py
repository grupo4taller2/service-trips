from uuid import UUID
from sqlalchemy.orm import Session

from src.database.requested_trip_dto import RequestedTripDTO
from src.database.taken_trip_dto import TakenTripDTO

from src.repositories.base_repository import BaseRepository
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import TripFacade, AcceptedByDriverState
from src.domain.rider import Rider
from src.domain.driver import Driver
from src.domain.directions import Directions
from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance

from src.utils.formatters import TimeFormatter, DistanceFormatter


class TripMapper:
    def joined_sql_to_trip(self, sql_trip):
        dict_form = dict(sql_trip)
        requested = dict_form['RequestedTripDTO']
        taken = dict_form['TakenTripDTO']

        rider: Rider = Rider(requested.rider_username)
        origin: Location = Location(requested.origin_address,
                                    requested.origin_latitude,
                                    requested.origin_longitude)

        destination: Location = Location(requested.destination_address,
                                         requested.destination_latitude,
                                         requested.destination_longitude)

        time: Time = Time(requested.estimated_time,
                          TimeFormatter().format(requested.estimated_time))

        distance: Distance = Distance(
            requested.distance,
            DistanceFormatter().format(requested.distance))

        directions: Directions = Directions(origin,
                                            destination,
                                            time,
                                            distance)

        if requested.state == 'looking_for_driver':
            state = TripFacade().create_from_name('looking_for_driver')

        elif requested.state == 'accepted_by_driver':
            driver_location = Location('unknown',
                                       taken.driver_latitude,
                                       taken.driver_longitude)
            driver: Driver = Driver(taken.driver_username,
                                    driver_location)
            state = AcceptedByDriverState(driver)

        return Trip(
            id=UUID(requested.id),
            rider=rider,
            directions=directions,
            type=requested.type,
            state=state,
            estimated_price=requested.estimated_price)

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

        if sql_trip.state == 'looking_for_driver':
            state = TripFacade().create_from_name('looking_for_driver')

        elif sql_trip.state == 'accepted_by_driver':
            driver_location = Location('unknown',
                                       sql_trip.driver_latitude,
                                       sql_trip.driver_longitude)
            driver: Driver = Driver(sql_trip.driver_username,
                                    driver_location)
            state = AcceptedByDriverState(driver)

        return Trip(
            id=UUID(sql_trip.id),
            rider=rider,
            directions=directions,
            type=sql_trip.type,
            state=state,
            estimated_price=sql_trip.estimated_price)


class TripRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def save(self, trip: Trip):
        trip_dto = RequestedTripDTO.from_entity(trip)
        self.session.add(trip_dto)

    def update(self, trip: Trip):
        if trip.state.name != 'accepted_by_driver':
            pass
        state_update = {
            RequestedTripDTO.state: trip.state.name
        }

        self.session.query(RequestedTripDTO) \
            .filter_by(id=str(trip.id)) \
            .update(state_update)

        self.session.flush()

        taken_trip_dto = TakenTripDTO.from_entity(trip)
        self.session.add(taken_trip_dto)
        self.seen.add(trip)

    def find_by_id(self, id: str):
        trip_dto = self.session \
            .query(RequestedTripDTO, TakenTripDTO) \
            .outerjoin(TakenTripDTO, RequestedTripDTO.id == TakenTripDTO.id) \
            .filter(RequestedTripDTO.id == id) \
            .one()

        mapper = TripMapper()
        trip = mapper.joined_sql_to_trip(trip_dto)
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
