from fastapi import APIRouter, status

from src.domain.directions import Directions

from src.domain import commands
from src.service_layer import messagebus
from src.repositories.dummy_unit_of_work import DummyUnitOfWork

from src.webapi.v1.directions.req_res_directions_models import (
    DirectionsResponse
)


router = APIRouter()


@router.get(
    '/search',
    status_code=status.HTTP_200_OK,
    response_model=DirectionsResponse
)
async def search_directions(origin: str = '', destination: str = ''):
    cmd = commands.DirectionsSearchCommand(origin=origin,
                                           destination=destination)
    uow = DummyUnitOfWork()
    directions: Directions = messagebus.handle(cmd, uow)[0]
    return DirectionsResponse(
        origin_address=directions.origin.address,
        origin_latitude=directions.origin.latitude,
        origin_longitude=directions.origin.longitude,
        destination_address=directions.destination.address,
        destination_latitude=directions.destination.latitude,
        destination_longitude=directions.destination.longitude,
        estimated_time=directions.time.seconds,
        distance=directions.distance.meters
    )
