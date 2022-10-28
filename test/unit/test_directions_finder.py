from src.conf.config import Settings
from src.domain.directions import Directions
from src.domain.directions_finder import DirectionsFinder


def test_directions_finder_fiuba():
    ORIGIN = 'Av. Paseo Colón 850, Buenos Aires'
    DESTINATION = 'Gral. Las Heras 2214, Buenos Aires'

    finder = DirectionsFinder(Settings().APP_ENV)
    found_directions: Directions = finder.find_by_address(ORIGIN, DESTINATION)
    assert found_directions.origin.address == ORIGIN
    assert found_directions.destination.address == DESTINATION
    assert found_directions.distance.repr == '5.7 km'
    assert found_directions.time.repr == '17 mins'
