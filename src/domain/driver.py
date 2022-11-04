from src.domain.location import Location


class Driver:
    def __init__(self, username, location: Location):
        self.username: str = username
        self.location: Location = location

    def take(self, trip):
        accepted_trip = trip.taken_by(self)
        self.current_trip = accepted_trip
