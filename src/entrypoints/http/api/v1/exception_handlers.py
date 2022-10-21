from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from src.service_layer.exceptions import (
    LocationNotFoundException
)


async def location_not_found_exception(
        request: Request,
        exc: LocationNotFoundException) -> JSONResponse:

    msg = f'Ubicación {str(exc)} no encontrada'
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': msg}
    )
