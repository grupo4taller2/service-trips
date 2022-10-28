from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance


class Directions:
    def __init__(self,
                 origin: Location,
                 destination: Location,
                 time: Time,
                 distance: Distance):

        self.origin = origin
        self.destination = destination
        self.time = time
        self.distance = distance
