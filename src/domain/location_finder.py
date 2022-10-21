import requests

from src.conf.config import Settings
from src.domain.location import Location
from src.service_layer.exceptions import (
    LocationNotFoundException,
    LocationServiceUnavailableException
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
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    API_KEY = Settings().GEOCODING_API_KEY

    def location_from_response(self, address, response):
        results = response.json()['results']
        if len(results) == 0:
            raise LocationNotFoundException(address)
        found = results[0]
        latitude = found['geometry']['location']['lat']
        longitude = found['geometry']['location']['lng']
        return Location(address, latitude, longitude)

    def find_by_address(self, address: str):
        endpoint = f"{self.BASE_URL}?address={address}&key={self.API_KEY}"
        response = requests.get(endpoint)

        if response.status_code == 200:
            return self.location_from_response(address, response)

        raise LocationServiceUnavailableException


class LocationFinder:
    def __init__(self, env: str):
        if Settings().APP_ENV == Settings().PROD_ENV:
            self.impl = GMapsLocationFinder()
        else:
            self.impl = DummyLocationFinder()

    def find_by_address(self, address: str):
        return self.impl.find_by_address(address)
