"""FastAPI entrypoint."""

from fastapi import FastAPI

from app.config import settings
from app.routers.analysis import router as analysis_router
from app.routers.health import router as health_router
from app.routers.imagery import router as imagery_router
from app.routers.parcel import router as parcel_router
from app.routers.scoring import router as scoring_router
from app.utils.logging import configure_logging

configure_logging()

app = FastAPI(title=settings.service_name, version=settings.app_version)
app.include_router(health_router)
app.include_router(imagery_router)
app.include_router(parcel_router)
app.include_router(analysis_router)
app.include_router(scoring_router)
