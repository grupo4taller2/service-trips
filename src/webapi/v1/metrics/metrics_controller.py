from fastapi import APIRouter, status
from src.metrics.metrics import FiuberMetrics
from fastapi import Response

router = APIRouter()


@router.get(
    '',
    status_code=status.HTTP_200_OK,
)
async def metrics_controller():
    return Response(content=FiuberMetrics.latest())
