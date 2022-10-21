from src.domain.commands import LocationSearchCommand
from src.service_layer.abstract_unit_of_work import AbstractUnitOfWork
from src.conf.config import Settings

from src.domain.location_finder import LocationFinder


def search_location(cmd: LocationSearchCommand, uow: AbstractUnitOfWork):
    location_finder = LocationFinder(Settings().APP_ENV)
    location = location_finder.find_by_address(cmd.address)
    return location
