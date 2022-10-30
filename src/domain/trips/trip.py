from uuid import UUID
from src.domain.directions import Directions
from src.domain.rider import Rider
from src.domain.trips.trip_state import TripState


class Trip:
    def __init__(self, id, rider, directions, type, state, estimated_price):
        self.id: UUID = id
        self.rider: Rider = rider
        self.directions: Directions = directions
        self.type: str = type
        self.state: TripState = state
        self.estimated_price = estimated_price
