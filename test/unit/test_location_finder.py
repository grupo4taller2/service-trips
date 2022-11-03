from src.domain.location_finder import LocationFinder
from src.conf.config import Settings


def test_location_finder_creation():
    finder = LocationFinder(Settings().APP_ENV)
    assert finder is not None


def test_location_finder():
    finder = LocationFinder(Settings().APP_ENV)
    found = finder.find_by_address('Av. Paseo Colón 850, Buenos Aires')
    assert found.address == 'Av. Paseo Colón 850, Buenos Aires'
