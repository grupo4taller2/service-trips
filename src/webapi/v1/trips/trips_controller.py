from fastapi import APIRouter, status
from src.domain.trips.trip import Trip
from typing import List, Optional

from src.domain import commands
from src.service_layer import messagebus
from src.repositories.unit_of_work import UnitOfWork
from src.notifications.notification_rider import sendNotification
from src.notifications.notification_drivers import sendNotificationDrivers

from src.webapi.v1.trips.req_res_trips_models import (
    TripRequestRequest,
    TripResponse,
    LocationResponse,
    TripPatchRequest,
)

router = APIRouter()


class TripResponseFormatter:

    def format(self, trip: Trip) -> TripResponse:
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
        ongoing_states = [
            'accepted_by_driver',
            'driver_arrived',
            'start_confirmed_by_driver',
            'finished_confirmed_by_driver',

        ]
        if trip.state.name in ongoing_states:
            return TripResponse(
                id=str(trip.id),
                rider_username=trip.rider.username,
                origin=origin_response,
                destination=destination_response,
                estimated_time=trip.directions.time.repr,
                estimated_price=trip.estimated_price,
                type=trip.type,
                distance=trip.directions.distance.repr,
                state=trip.state.name,
                driver_username=trip.state.driver_username(),
                driver_latitude=trip.state.driver_latitude(),
                driver_longitude=trip.state.driver_longitude()
            )

        return TripResponse(
            id=str(trip.id),
            rider_username=trip.rider.username,
            origin=origin_response,
            destination=destination_response,
            estimated_time=trip.directions.time.repr,
            estimated_price=trip.estimated_price,
            type=trip.type,
            distance=trip.directions.distance.repr,
            state=trip.state.name
        )


@router.get(
    '/{trip_id}',
    status_code=status.HTTP_200_OK,
    response_model=TripResponse,
)
async def trip_get(trip_id: str):
    cmd = commands.TripGetCommand(
        id=trip_id
    )
    uow = UnitOfWork()
    trip: Trip = messagebus.handle(cmd, uow)[0]
    formatter = TripResponseFormatter()
    return formatter.format(trip)


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

    print(trip.state.name)
    if (trip.state.name == 'looking_for_driver'):
        sendNotificationDrivers()

    return TripResponse(
        id=str(trip.id),
        rider_username=trip.rider.username,
        origin=origin_response,
        destination=destination_response,
        estimated_time=trip.directions.time.repr,
        estimated_price=trip.estimated_price,
        type=trip.type,
        distance=trip.directions.distance.repr,
        state=trip.state.name
    )


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=List[TripResponse]
)
async def get_trips_for_driver_with_state_offset_limit(
        driver_username: Optional[str] = None,
        trip_state: Optional[str] = None,
        offset: Optional[float] = None,
        limit: Optional[float] = None):

    cmd = commands.TripGetForDriver(
        driver_username=driver_username,
        trip_state=trip_state,
        offset=offset,
        limit=limit
    )
    uow = UnitOfWork()
    trips = messagebus.handle(cmd, uow)[0]
    formatter = TripResponseFormatter()
    return [formatter.format(trip) for trip in trips]


@router.patch(
    '/{trip_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TripResponse
)
async def trip_patch(trip_id: str, req: TripPatchRequest):
    cmd = commands.TripUpdateCommand(
        trip_id=trip_id,
        driver_username=req.driver_username,
        driver_latitude=req.driver_current_latitude,
        driver_longitude=req.driver_current_longitude,
        trip_state=req.trip_state,
    )
    uow = UnitOfWork()
    trip = messagebus.handle(cmd, uow)[0]
    formatter = TripResponseFormatter()
    trip_resp = formatter.format(trip)

    if (req.trip_state == 'accepted_by_driver'):
        sendNotification(trip_resp.rider_username, trip_resp.driver_username)

    return trip_resp
