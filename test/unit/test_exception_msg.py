from src.service_layer.exceptions import (
    LocationNotFoundException,
    LocationServiceUnavailableException,
    DirectionsNotFoundException,
    DirectionsServiceUnavailableException,
    PricingServiceUnavailableException,
    TripNotFoundException
)


def test_location_not_found():
    try:
        raise LocationNotFoundException('Paseo Colón 850')
    except LocationNotFoundException as e:
        assert e.message == 'Paseo Colón 850'
    try:
        raise LocationNotFoundException
    except LocationNotFoundException as e:
        assert str(e) == 'No encontrada'


def test_location_service_not_found():
    try:
        raise LocationServiceUnavailableException('503')
    except LocationServiceUnavailableException as e:
        assert e.message == '503'
    try:
        raise LocationServiceUnavailableException
    except LocationServiceUnavailableException as e:
        assert str(e) == 'No disponible'


def test_directions_not_found():
    MSG = 'origin: Paseo Colón 850,destination: Las Heras 2214'
    try:
        raise DirectionsNotFoundException('Paseo Colón 850', 'Las Heras 2214')
    except DirectionsNotFoundException as e:
        assert e.message == MSG
    try:
        raise DirectionsNotFoundException
    except DirectionsNotFoundException as e:
        assert str(e) == 'No encontrada'


def test_direction_service_unavailable():
    try:
        raise DirectionsServiceUnavailableException('503')
    except DirectionsServiceUnavailableException as e:
        assert e.message == '503'
    try:
        raise DirectionsServiceUnavailableException
    except DirectionsServiceUnavailableException as e:
        assert str(e) == 'No disponible'


def test_pricing_service_unavailable():
    try:
        raise PricingServiceUnavailableException('503')
    except PricingServiceUnavailableException as e:
        assert e.message == '503'
    try:
        raise PricingServiceUnavailableException
    except PricingServiceUnavailableException as e:
        assert str(e) == 'No disponible'


def test_trip_not_found():
    try:
        raise TripNotFoundException('ca0043b8-b2a8-4746-9925-a8d3709d2b6c')
    except TripNotFoundException as e:
        assert e.message == 'ca0043b8-b2a8-4746-9925-a8d3709d2b6c'
    try:
        raise TripNotFoundException
    except TripNotFoundException as e:
        assert str(e) == 'No encontrado'
