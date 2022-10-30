from fastapi import APIRouter

from src.webapi.v1 import (
    healthcheck
)

from src.webapi.v1.locations import locations_controller
from src.webapi.v1.directions import directions_controller
from src.webapi.v1.trips import trips_controller


api_router = APIRouter()

api_router.include_router(healthcheck.router,
                          prefix="/healthcheck",
                          tags=["healthcheck"])

api_router.include_router(locations_controller.router,
                          prefix='/locations',
                          tags=['locations'])

api_router.include_router(directions_controller.router,
                          prefix='/directions',
                          tags=['directions'])

api_router.include_router(trips_controller.router,
                          prefix='/trips',
                          tags=['trips'])
