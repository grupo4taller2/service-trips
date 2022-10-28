from fastapi import FastAPI, APIRouter

from src.conf.config import Settings
from src.webapi.v1 import api
from src.service_layer.exceptions import (
    DirectionsNotFoundException,
    LocationNotFoundException,
    LocationServiceUnavailableException
)
from src.webapi.v1.exception_handlers import (
    location_not_found_exception,
    location_service_unavailable_exception,
    directions_not_found_exception
)

root_router = APIRouter()
app = FastAPI(title="Trips API", openapi_url="/openapi.json")

app.include_router(api.api_router, prefix=Settings().API_V1_STR)
app.include_router(root_router)

app.add_exception_handler(LocationNotFoundException,
                          location_not_found_exception)
app.add_exception_handler(LocationServiceUnavailableException,
                          location_service_unavailable_exception)
app.add_exception_handler(DirectionsNotFoundException,
                          directions_not_found_exception)
