from fastapi import APIRouter

from src.webapi.v1 import (
    healthcheck
)

from src.webapi.v1.locations import (
    locations_controller
)


api_router = APIRouter()

api_router.include_router(healthcheck.router,
                          prefix="/healthcheck",
                          tags=["healthcheck"])

api_router.include_router(locations_controller.router,
                          prefix='/locations',
                          tags=['locations'])
