from sqlalchemy.orm import Session
from src.database.requested_trip_dto import RequestedTripDTO

from src.repositories.base_repository import BaseRepository
from src.domain.trips.trip import Trip


class TripRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def save(self, trip: Trip):
        trip_dto = RequestedTripDTO.from_entity(trip)
        self.session.add(trip_dto)

    def update(self, trip: Trip):
        pass
