from src.domain.commands import (
    DirectionsSearchCommand,
    LocationSearchCommand
)
from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from src.conf.config import Settings

from src.domain.location_finder import LocationFinder
from src.domain.directions_finder import DirectionsFinder


def search_location(cmd: LocationSearchCommand, uow: AbstractUnitOfWork):
    location_finder = LocationFinder(Settings().APP_ENV)
    location = location_finder.find_by_address(cmd.address)
    return location


def search_directions(cmd: DirectionsSearchCommand, uow: AbstractUnitOfWork):
    directions_finder = DirectionsFinder(Settings().APP_ENV)
    directions = directions_finder.find_by_address(cmd.origin, cmd.destination)
    return directions
