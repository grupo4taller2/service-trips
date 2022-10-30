from uuid import uuid4

from src.conf.config import Settings

from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from src.external.price_estimator import PriceEstimator

from src.domain.commands import (
    DirectionsSearchCommand,
    LocationSearchCommand,
    TripRequestCommand,
    TripGetCommand
)

from src.domain.location_finder import LocationFinder
from src.domain.directions_finder import DirectionsFinder
from src.domain.trips.trip import Trip
from src.domain.trips.trip_state import LookingForDriverState
from src.domain.rider import Rider


def search_location(cmd: LocationSearchCommand, uow: AbstractUnitOfWork):
    location_finder = LocationFinder(Settings().APP_ENV)
    location = location_finder.find_by_address(cmd.address)
    return location


def search_directions(cmd: DirectionsSearchCommand, uow: AbstractUnitOfWork):
    directions_finder = DirectionsFinder(Settings().APP_ENV)
    directions = directions_finder.find_by_address(cmd.origin, cmd.destination)
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
        return trip


def get_trip_by_id(cmd: TripGetCommand, uow: AbstractUnitOfWork):
    with uow:
        trip = uow.trip_repository.get_by_id(cmd.id)
        uow.commit()
        return trip
