from fastapi import APIRouter, status
from src.domain.trips.trip import Trip

from src.domain import commands
from src.service_layer import messagebus
from src.repositories.unit_of_work import UnitOfWork

from src.webapi.v1.trips.req_res_trips_models import (
    TripRequestRequest,
    TripResponse,
    LocationResponse
)

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=TripResponse
)
async def trip_request(cmd: TripRequestRequest):
    cmd = commands.TripRequestCommand(
        rider_username=cmd.rider_username,
        rider_origin_address=cmd.rider_origin_address,
        rider_destination_address=cmd.rider_destination_address,
        trip_type=cmd.trip_type
    )
    uow = UnitOfWork()
    trip: Trip = messagebus.handle(cmd, uow)[0]
    origin_response = LocationResponse(
        address=trip.directions.origin.address,
        latitude=trip.directions.origin.latitude,
        longitude=trip.directions.origin.longitude
    )
    destination_response = LocationResponse(
        address=trip.directions.destination.address,
        latitude=trip.directions.destination.latitude,
        longitude=trip.directions.destination.longitude
    )

    return TripResponse(
        id=str(trip.id),
        rider_username=trip.rider.username,
        origin=origin_response,
        destination=destination_response,
        estimated_time=trip.directions.time.repr,
        trip_type=trip.type,
        distance=trip.directions.distance.repr
    )
