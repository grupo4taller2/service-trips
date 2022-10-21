from src.domain.location import Location


def test_location_create():
    location = Location('Av. Paseo Colón 850, Buenos Aires',
                        -34.6174635,
                        -58.369979)
    assert location is not None


def test_location_create_address():
    ADDRESS = 'Av. Paseo Colón 850, Buenos Aires'
    location = Location(ADDRESS,
                        -34.6174635,
                        -58.369979)
    assert location.address == ADDRESS


def test_location_create_latitude():
    LATITUDE = -34.6174635
    location = Location('Av. Paseo Colón 850, Buenos Aires',
                        LATITUDE,
                        -58.369979)
    assert location.latitude == LATITUDE


def test_location_create_longitude():
    LONGITUDE = -58.369979
    location = Location('Av. Paseo Colón 850, Buenos Aires',
                        -34.6174635,
                        LONGITUDE)
    assert location.longitude == LONGITUDE
