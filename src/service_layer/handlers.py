from uuid import uuid4
from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from src.conf.config import Settings

from src.domain.commands import (
    DirectionsSearchCommand,
    LocationSearchCommand,
    TripStartCommand
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


def start_trip(cmd: TripStartCommand, uow: AbstractUnitOfWork):
    id = uuid4()
    rider = Rider(cmd.rider_username)
    directions_finder = DirectionsFinder(Settings().APP_ENV)
    directions = directions_finder.find_by_address(
        cmd.rider_origin_address,
        cmd.rider_destination_address
    )
    state = LookingForDriverState()
    trip: Trip = Trip(id, rider, directions, cmd.trip_type, state)
    with uow:
        uow.trip_repository.save(trip)
        uow.commit()
        return trip
