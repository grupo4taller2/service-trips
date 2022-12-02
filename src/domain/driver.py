from src.domain.location import Location


class Driver:
    def __init__(self, username, location: Location):
        self.username: str = username
        self.location: Location = location

    def update(self, trip, state):
        updated_trip = trip.update(self, state)
        self.current_trip = updated_trip
        return updated_trip
