from src.conf.config import Settings
from src.domain.driver import Driver
from src.domain.location import Location
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import (
    TripFacade,
    AcceptedByDriverState,
    DriverWaitingState,
    OngoingState,
    FinishedState
)
from src.domain.directions_finder import DirectionsFinder


def test_driver_name():
    location: Location = Location('unkwnown',
                                  -33.0,
                                  -58.0)
    driver: Driver = Driver('mateo', location)
    assert driver.username == 'mateo'
    assert driver.location.latitude == -33.0
    assert driver.location.longitude == -58.0


def test_driver_take_trip():
    OBELISCO_LATITUD = -34.6037345
    OBELISCO_LONGITUD = -58.3837591

    obelisco: Location = Location('obelisco',
                                  OBELISCO_LATITUD,
                                  OBELISCO_LONGITUD)

    driver: Driver = Driver('mateo', obelisco)
    finder: DirectionsFinder = DirectionsFinder(Settings().TEST_ENV)
    directions = finder.find_by_address('Av. Paseo Colón 850, Buenos Aires',
                                        'Gral. Las Heras 2214, Buenos Aires')
    trip: Trip = Trip('fakeid',
                      'rider_username',
                      directions,
                      'regular',
                      TripFacade().create_from_name('looking_for_driver'),
                      '0.02')
    new_state = TripFacade.create_from_name('accepted_by_driver', driver)
    driver.update(trip, new_state)
    assert trip.state == AcceptedByDriverState(driver)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD


def test_driver_arrived():
    OBELISCO_LATITUD = -34.6037345
    OBELISCO_LONGITUD = -58.3837591

    obelisco: Location = Location('obelisco',
                                  OBELISCO_LATITUD,
                                  OBELISCO_LONGITUD)

    driver: Driver = Driver('mateo', obelisco)
    finder: DirectionsFinder = DirectionsFinder(Settings().TEST_ENV)
    directions = finder.find_by_address('Av. Paseo Colón 850, Buenos Aires',
                                        'Gral. Las Heras 2214, Buenos Aires')
    trip: Trip = Trip('fakeid',
                      'rider_username',
                      directions,
                      'regular',
                      TripFacade().create_from_name('looking_for_driver'),
                      '0.02')
    new_state = TripFacade.create_from_name('accepted_by_driver', driver)
    driver.update(trip, new_state)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name('driver_arrived', driver)
    driver.update(trip, new_state)
    assert trip.state == DriverWaitingState(driver)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD


def test_driver_start_trip():
    OBELISCO_LATITUD = -34.6037345
    OBELISCO_LONGITUD = -58.3837591

    obelisco: Location = Location('obelisco',
                                  OBELISCO_LATITUD,
                                  OBELISCO_LONGITUD)

    driver: Driver = Driver('mateo', obelisco)
    finder: DirectionsFinder = DirectionsFinder(Settings().TEST_ENV)
    directions = finder.find_by_address('Av. Paseo Colón 850, Buenos Aires',
                                        'Gral. Las Heras 2214, Buenos Aires')
    trip: Trip = Trip('fakeid',
                      'rider_username',
                      directions,
                      'regular',
                      TripFacade().create_from_name('looking_for_driver'),
                      '0.02')
    new_state = TripFacade.create_from_name('accepted_by_driver', driver)
    driver.update(trip, new_state)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name('driver_arrived', driver)
    driver.update(trip, new_state)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name(
        'start_confirmed_by_driver',
        driver)
    driver.update(trip, new_state)
    assert trip.state == OngoingState(driver)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD


def test_driver_finish_trip():
    OBELISCO_LATITUD = -34.6037345
    OBELISCO_LONGITUD = -58.3837591

    obelisco: Location = Location('obelisco',
                                  OBELISCO_LATITUD,
                                  OBELISCO_LONGITUD)

    driver: Driver = Driver('mateo', obelisco)
    finder: DirectionsFinder = DirectionsFinder(Settings().TEST_ENV)
    directions = finder.find_by_address('Av. Paseo Colón 850, Buenos Aires',
                                        'Gral. Las Heras 2214, Buenos Aires')
    trip: Trip = Trip('fakeid',
                      'rider_username',
                      directions,
                      'regular',
                      TripFacade().create_from_name('looking_for_driver'),
                      '0.02')
    new_state = TripFacade.create_from_name('accepted_by_driver', driver)
    driver.update(trip, new_state)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name('driver_arrived', driver)
    driver.update(trip, new_state)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name(
        'start_confirmed_by_driver',
        driver)
    driver.update(trip, new_state)
    assert trip.state == OngoingState(driver)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
    new_state = TripFacade.create_from_name(
        'finished_confirmed_by_driver',
        driver)
    driver.update(trip, new_state)
    assert trip.state == FinishedState(driver)
    assert trip.driver_username() == 'mateo'
    assert trip.driver_latitude() == OBELISCO_LATITUD
    assert trip.driver_longitude() == OBELISCO_LONGITUD
