"""Scoring and provider status router."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/v1", tags=["scoring"])


@router.get("/providers/status")
async def providers_status() -> dict:
    return {
        "google_geocoding": bool(settings.google_geocoding_api_key),
        "mapbox_imagery": bool(settings.mapbox_api_token),
        "arcgis_imagery": True,
        "osm_roads": True,
        "county_gis": "stubbed",
    }
