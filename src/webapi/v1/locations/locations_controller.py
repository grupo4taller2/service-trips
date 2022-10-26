from fastapi import APIRouter, status

from src.domain.location import Location

from src.domain import commands
from src.service_layer import messagebus
from src.repositories.dummy_unit_of_work import DummyUnitOfWork

from src.webapi.v1.locations.req_res_location_models import (
    LocationResponse
)


router = APIRouter()


@router.get(
    '/search/',
    status_code=status.HTTP_200_OK,
    response_model=LocationResponse
)
async def search_location(address: str = ''):
    cmd = commands.LocationSearchCommand(address=address)
    uow = DummyUnitOfWork()
    location: Location = messagebus.handle(cmd, uow)[0]
    return LocationResponse(address=location.address,
                            latitude=location.latitude,
                            longitude=location.longitude)
