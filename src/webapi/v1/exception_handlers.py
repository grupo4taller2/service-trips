from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.service_layer.exceptions import (
    DirectionsNotFoundException,
    LocationNotFoundException,
    LocationServiceUnavailableException
)


def location_not_found_exception(
        request: Request,
        exc: LocationNotFoundException) -> JSONResponse:

    msg = f'Ubicación {str(exc)} no encontrada'
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': msg}
    )


def location_service_unavailable_exception(
        request: Request,
        exc: LocationServiceUnavailableException) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={'message': str(exc)}
    )


def directions_not_found_exception(
        request: Request,
        exc: DirectionsNotFoundException) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': str(exc)}
    )
