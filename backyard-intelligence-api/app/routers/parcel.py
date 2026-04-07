"""Parcel router."""

from fastapi import APIRouter, Depends

from app.dependencies import get_geocoding_service, get_parcel_service
from app.models.request_models import AddressRequest
from app.services.geocoding_service import GeocodingService
from app.services.parcel_service import ParcelService
from app.utils.geometry import polygon_geojson

router = APIRouter(prefix="/v1", tags=["parcel"])


@router.post("/parcel-lookup")
async def parcel_lookup(
    req: AddressRequest,
    geocoder: GeocodingService = Depends(get_geocoding_service),
    parcel_service: ParcelService = Depends(get_parcel_service),
) -> dict:
    geocode = await geocoder.geocode(req.address)
    parcel = await parcel_service.lookup(geocode["latitude"], geocode["longitude"])
    if not parcel:
        return {"parcel_found": False, "warnings": ["Parcel data unavailable in current jurisdiction feed."]}
    return {
        "parcel_found": True,
        "parcel_id": parcel["parcel_id"],
        "jurisdiction": parcel["jurisdiction"],
        "lot_area_sqft": parcel["lot_area_sqft"],
        "zoning": parcel["zoning"],
        "geometry": polygon_geojson(parcel["geometry"]),
    }
