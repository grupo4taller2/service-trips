from src.domain.directions import Directions
from src.domain.rider import Rider
from src.domain.trips.trip_state import TripState


class Trip:
    def __init__(self, id, rider, directions, type):
        self.id: str = id
        self.rider: Rider = rider
        self.directions: Directions = directions
        self.type: TripState = type
