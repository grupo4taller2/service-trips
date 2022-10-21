from src.conf.config import Settings
from src.domain.location import Location
from src.service_layer.exceptions import (
    LocationNotFoundException
)

FAKE_LOCATION_SOURCE = {
    'Av. Paseo Colón 850, Buenos Aires': Location(
        'Av. Paseo Colón 850, Buenos Aires',
        -34.6174635,
        -58.369979
    )
}


class DummyLocationFinder:
    def __init__(self):
        global FAKE_LOCATION_SOURCE
        self.locations = FAKE_LOCATION_SOURCE

    def find_by_address(self, address: str):
        try:
            return self.locations[address]
        except KeyError:
            raise LocationNotFoundException(address)


class GMapsLocationFinder:
    pass


class LocationFinder:
    def __init__(self, env: str):
        if Settings().APP_ENV == Settings().TEST_ENV:
            self.impl = DummyLocationFinder()
        else:
            self.impl = GMapsLocationFinder()

    def find_by_address(self, address: str):
        return self.impl.find_by_address(address)
