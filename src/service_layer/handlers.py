from uuid import uuid4

from src.conf.config import Settings

from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from src.external.price_estimator import PriceEstimator

from src.metrics.metrics import FiuberMetrics

from src.domain.commands import (
    DirectionsSearchCommand,
    LocationSearchCommand,
    TripRequestCommand,
    TripGetCommand,
    TripGetForDriver,
    TripUpdateCommand
)

from src.domain.location_finder import LocationFinder
from src.domain.directions_finder import DirectionsFinder
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import TripFacade
from src.domain.trips.trip_state import LookingForDriverState
from src.domain.rider import Rider
from src.domain.driver import Driver
from src.domain.location import Location


def search_location(cmd: LocationSearchCommand, uow: AbstractUnitOfWork):
    location_finder = LocationFinder(Settings().APP_ENV)
    location = location_finder.find_by_address(cmd.address)
    FiuberMetrics.count_event(FiuberMetrics.LocationSearched)
    return location


def search_directions(cmd: DirectionsSearchCommand, uow: AbstractUnitOfWork):
    directions_finder = DirectionsFinder(Settings().APP_ENV)
    directions = directions_finder.find_by_address(cmd.origin, cmd.destination)
    FiuberMetrics.count_event(FiuberMetrics.DirectionsSearched)
    return directions


def request_trip(cmd: TripRequestCommand, uow: AbstractUnitOfWork):
    id = uuid4()
    rider = Rider(cmd.rider_username)
    directions_finder = DirectionsFinder(Settings().APP_ENV)
    directions = directions_finder.find_by_address(
        cmd.rider_origin_address,
        cmd.rider_destination_address
    )
    price_estimator = PriceEstimator()
    estimated_price = price_estimator.estimate_for(rider, directions)
    state = LookingForDriverState()
    trip: Trip = Trip(id,
                      rider,
                      directions,
                      cmd.trip_type,
                      state,
                      estimated_price)
    with uow:
        uow.trip_repository.save(trip)
        uow.commit()
    FiuberMetrics.count_trip_update(state.name)
    return trip


def get_trip_by_id(cmd: TripGetCommand, uow: AbstractUnitOfWork):
    with uow:
        trip = uow.trip_repository.find_by_id(cmd.id)
        uow.commit()
        return trip


def get_trips_for_driver(cmd: TripGetForDriver, uow: AbstractUnitOfWork):
    with uow:
        trips = uow.trip_repository.find_for_driver_state_offset_limit(
            cmd.driver_username,
            cmd.trip_state,
            cmd.offset,
            cmd.limit
        )
        uow.commit()
        return trips


def trip_update(cmd: TripUpdateCommand, uow: AbstractUnitOfWork):
    with uow:
        trip: Trip = uow.trip_repository.find_by_id(cmd.trip_id)
        location: Location = Location('unknown',
                                      cmd.driver_latitude,
                                      cmd.driver_longitude)
        driver: Driver = Driver(cmd.driver_username,
                                location)
        state = TripFacade.create_from_name(cmd.trip_state, driver)
        driver.update(trip, state)
        trip = uow.trip_repository.update(trip)
        uow.commit()
        FiuberMetrics.count_trip_update(state.name)
        return trip
