from fastapi import APIRouter, status
from src.metrics.metrics import FiuberMetrics
from fastapi import Response
from fastapi.responses import JSONResponse
from src.repositories.unit_of_work import UnitOfWork


router = APIRouter()


@router.get(
    '',
    status_code=status.HTTP_200_OK,
)
async def metrics_controller():
    FiuberMetrics.record()
    return Response(content=FiuberMetrics.latest())


@router.get(
    '/{driver_username}',
    status_code=status.HTTP_200_OK,
)
async def metrics_driver_trips_controller(driver_username):
    with UnitOfWork() as uow:
        repo = uow.trip_repository
        n_trips = repo.trips_for_driver(driver_username)
        return JSONResponse({
            'finished_trips': n_trips
        })


def format_trips(trips):
    return [
        {
            'driver_username': t[0],
            'distance': t[1],
            'rider_username': t[2],
            'estimataed_time': t[3],
            'estimated_price': t[4],

        }
        for t in trips
    ]


@router.get(
    '/trips/{minutes}',
    status_code=status.HTTP_200_OK,
)
async def trips_in_last_minutes(minutes):
    with UnitOfWork() as uow:
        repo = uow.trip_repository
        trips = repo.trips_last_minutes(minutes)
        return format_trips(trips)
