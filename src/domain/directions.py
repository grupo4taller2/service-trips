from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance


class Directions:
    def __init__(self,
                 location_from: Location,
                 location_to: Location,
                 time: Time,
                 distance: Distance):

        self.location_from = location_from
        self.location_to = location_to
        self.time = time
        self.distance = distance
