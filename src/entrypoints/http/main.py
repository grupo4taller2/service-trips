from fastapi import FastAPI, APIRouter

from src.conf.config import Settings
from src.entrypoints.http.api.v1 import api
from src.service_layer.exceptions import (
    LocationNotFoundException,
    LocationServiceUnavailableException
)
from src.entrypoints.http.api.v1.exception_handlers import (
    location_not_found_exception,
    location_service_unavailable_exception
)

root_router = APIRouter()
app = FastAPI(title="Trips API", openapi_url="/openapi.json")

app.include_router(api.api_router, prefix=Settings().API_V1_STR)
app.include_router(root_router)

app.add_exception_handler(LocationNotFoundException,
                          location_not_found_exception)
app.add_exception_handler(LocationServiceUnavailableException,
                          location_service_unavailable_exception)
