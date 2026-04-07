"""Health router."""

from fastapi import APIRouter

from app.config import settings
from app.models.response_models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.service_name, version=settings.app_version)
