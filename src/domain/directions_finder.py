import requests
from src.service_layer.exceptions import (
    DirectionsNotFoundException,
    DirectionsServiceUnavailableException
)

from src.conf.config import Settings
from src.domain.location import Location
from src.domain.time import Time
from src.domain.distance import Distance
from src.domain.directions import Directions


class DummyDirectionsFinder:
    def __init__(self):
        self.paseo_colon = Location(
            'Av. Paseo Colón 850, Buenos Aires',
            -34.6174635,
            -58.369979
        )
        self.las_heras = Location(
            'Gral. Las Heras 2214, Buenos Aires',
            -34.5884291,
            -58.39608870000001
        )

    def find_by_address(self, origin: str, destination: str):
        if origin == self.paseo_colon.address and \
                destination == self.las_heras.address:

            return Directions(self.paseo_colon,
                              self.las_heras,
                              Time(17*60, '17 mins'),
                              Distance(5704, '5.7 km'))

        elif origin == self.las_heras.address and \
                destination == self.paseo_colon.address:

            return Directions(self.las_heras,
                              self.paseo_colon,
                              Time(17*60, '17 mins'),
                              Distance(5704, '5.7 km'))
        raise DirectionsNotFoundException(origin, destination)


class GMapsDirectionsFinder:
    BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"
    API_KEY = Settings().GEOCODING_API_KEY
    NOT_FOUND_STATUS = 'NOT_FOUND'

    def directions_from_response(self, response, origin, destination):
        status = response.json()['status']
        if status == self.NOT_FOUND_STATUS:
            raise DirectionsNotFoundException(origin, destination)

        results = response.json()['routes'][0]['legs'][0]

        origin_latitude = results['start_location']['lat']
        origin_longitude = results['start_location']['lng']
        origin_location = Location(origin, origin_latitude, origin_longitude)

        destination_latitude = results['end_location']['lat']
        destination_longitude = results['end_location']['lng']
        destination_location = Location(destination,
                                        destination_latitude,
                                        destination_longitude)

        duration_response = results['duration']
        duration = Time(duration_response['value'], duration_response['text'])

        distance_response = results['distance']
        distance = Distance(distance_response['value'],
                            distance_response['text'])

        return Directions(origin_location,
                          destination_location,
                          duration,
                          distance)

    def find_by_address(self, origin: str, destination: str):
        endpoint = f'{self.BASE_URL}'
        endpoint += f'?origin={origin}&destination={destination}'
        endpoint += f'&key={self.API_KEY}'
        response = requests.get(endpoint)
        if response.status_code == 200:
            return self.directions_from_response(response, origin, destination)
        elif response.status_code == 400:
            raise DirectionsNotFoundException(origin, destination)

        raise DirectionsServiceUnavailableException


class DirectionsFinder:
    def __init__(self, env: str):
        if Settings().APP_ENV == Settings().PROD_ENV:
            self.impl = GMapsDirectionsFinder()
        else:
            self.impl = DummyDirectionsFinder()

    def find_by_address(self, origin: str, destination: str):
        return self.impl.find_by_address(origin, destination)
