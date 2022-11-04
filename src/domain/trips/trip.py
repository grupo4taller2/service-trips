from uuid import UUID
from src.domain.directions import Directions
from src.domain.rider import Rider
from src.domain.trips.trip_state import TripState
from src.domain.driver import Driver


class Trip:
    def __init__(self, id, rider, directions, type, state, estimated_price):
        self.id: UUID = id
        self.rider: Rider = rider
        self.directions: Directions = directions
        self.type: str = type
        self.state: TripState = state
        self.estimated_price = estimated_price
        self.events = []

    def taken_by(self, driver: Driver):
        self.state = self.state.taken_by(driver)

    def driver_username(self):
        return self.state.driver_username()

    def driver_latitude(self):
        return self.state.driver_latitude()

    def driver_longitude(self):
        return self.state.driver_longitude()
