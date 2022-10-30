from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.database.requested_trip_dto import RequestedTripDTO

from src.repositories.base_repository import BaseRepository
from src.service_layer.exceptions import TripNotFoundException
from src.domain.trips.trip import Trip


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
