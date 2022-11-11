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
        self.events = []

    def driver_username(self):
        return self.state.driver_username()

    def driver_latitude(self):
        return self.state.driver_latitude()

    def driver_longitude(self):
        return self.state.driver_longitude()

    def update(self, driver, new_state):
        self.state = self.state.transition(driver, new_state)
        return self
