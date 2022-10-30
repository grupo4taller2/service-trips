from sqlalchemy.orm import Session

from src.repositories.base_repository import BaseRepository
from src.domain.trips.trip import Trip


class TripRepository(BaseRepository):
    def __init__(self, session):
        super().__init__()
        self.session: Session = session

    def save(self, trip: Trip):
        pass

    def update(self, trip: Trip):
        pass
