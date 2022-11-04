import requests

from src.conf.config import Settings
from src.domain.rider import Rider
from src.domain.directions import Directions
from src.service_layer.exceptions import PricingServiceUnavailableException


class DummyPriceEstimator:
    def estimate_for(self, rider: Rider, directions: Directions):
        return '0.035'


class FIUBERPriceEstimator:
    URL = Settings().PRICING_SERVICE_REMOTE_URL

    def estimate_for(self, rider: Rider, directions: Directions):
        params = {
            'rider_username': rider.username,
            'origin_address': directions.origin.address,
            'origin_latitude': directions.origin.latitude,
            'origin_longitude': directions.origin.longitude,
            'destination_address': directions.destination.address,
            'destination_latitude': directions.destination.latitude,
            'destination_longitude': directions.destination.longitude,
            'estimated_time': directions.time.seconds,
            'distance': directions.distance.meters,
        }
        response = requests.get(self.URL + '/estimations', params=params)
        if response.status_code != 200:
            raise PricingServiceUnavailableException

        value = response.json()['estimated_price']
        return value


class PriceEstimator:
    def __init__(self):
        if Settings().APP_ENV == Settings().PROD_ENV:
            self.impl = FIUBERPriceEstimator()
        else:
            self.impl = DummyPriceEstimator()

    def estimate_for(self, rider: Rider, directions: Directions):
        return self.impl.estimate_for(rider, directions)
