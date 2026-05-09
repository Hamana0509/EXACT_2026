from fastapi import APIRouter

from app.config import get_settings
from app.schemas.api import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model=get_settings().model_name)
