"""Scoring and provider status router."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="/v1", tags=["scoring"])


@router.get("/providers/status")
async def providers_status() -> dict:
    """Provider availability and configuration status."""
    return {
        "google_geocoding": {
            "configured": bool(settings.google_geocoding_api_key),
            "available": True,
        },
        "mapbox_imagery": {
            "configured": bool(settings.mapbox_api_token),
            "available": bool(settings.mapbox_api_token),
        },
        "arcgis_imagery": {
            "configured": True,
            "available": True,
        },
        "osm_roads": {
            "configured": True,
            "available": True,
        },
        "county_gis": {
            "configured": False,
            "available": "stubbed",
        },
    }
