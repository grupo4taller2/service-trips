from src.domain.location_finder import LocationFinder
from src.conf.config import Settings


def test_location_finder_creation():
    finder = LocationFinder(Settings().APP_ENV)
    assert finder is not None
