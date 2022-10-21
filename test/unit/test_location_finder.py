from src.domain.location_finder import LocationFinder


def test_location_finder_creation():
    finder = LocationFinder()
    assert finder is not None
