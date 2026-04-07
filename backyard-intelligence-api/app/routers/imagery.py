"""Imagery-related router."""

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_backyard_service,
    get_building_service,
    get_geocoding_service,
    get_imagery_service,
    get_orientation_service,
    get_parcel_service,
    get_roads_service,
)
from app.models.request_models import BackyardImageRequest
from app.models.response_models import BackyardImageResponse, GeocodeOut
from app.services.backyard_service import BackyardService
from app.services.building_service import BuildingService
from app.services.geocoding_service import GeocodingService
from app.services.imagery_service import ImageryService
from app.services.orientation_service import OrientationService
from app.services.parcel_service import ParcelService
from app.services.roads_service import RoadsService

router = APIRouter(prefix="/v1", tags=["imagery"])


@router.post("/backyard-image", response_model=BackyardImageResponse)
async def backyard_image(
    req: BackyardImageRequest,
    geocoder: GeocodingService = Depends(get_geocoding_service),
    parcel_service: ParcelService = Depends(get_parcel_service),
    building_service: BuildingService = Depends(get_building_service),
    roads_service: RoadsService = Depends(get_roads_service),
    orientation_service: OrientationService = Depends(get_orientation_service),
    backyard_service: BackyardService = Depends(get_backyard_service),
    imagery_service: ImageryService = Depends(get_imagery_service),
) -> BackyardImageResponse:
    geocode = await geocoder.geocode(req.address)
    parcel = await parcel_service.lookup(geocode["latitude"], geocode["longitude"])
    building = await building_service.lookup(geocode["latitude"], geocode["longitude"])
    road = await roads_service.nearest_road(geocode["latitude"], geocode["longitude"])
    front = orientation_service.infer_front_direction(parcel["geometry"], road) if parcel else None
    backyard = backyard_service.infer_backyard(geocode["latitude"], geocode["longitude"], parcel, building, front)

    centroid = backyard["centroid"]
    imagery_url = imagery_service.imagery_url(
        req.imagery_provider,
        centroid["latitude"],
        centroid["longitude"],
        req.zoom,
        req.width,
        req.height,
    )

    quality = 40
    if parcel:
        quality += 30
    if building:
        quality += 20
    if road:
        quality += 10

    return BackyardImageResponse(
        input_address=req.address,
        normalized_address=geocode["normalized_address"],
        geocode=GeocodeOut(latitude=geocode["latitude"], longitude=geocode["longitude"], place_id=geocode.get("place_id")),
        parcel_summary={k: v for k, v in parcel.items() if k != "geometry"} if parcel else None,
        building_summary={k: v for k, v in building.items() if k != "geometry"} if building else None,
        backyard_centroid=centroid,
        backyard_confidence=backyard["confidence"],
        imagery_provider=req.imagery_provider,
        imagery_url=imagery_url,
        fallback_used=backyard["fallback_used"],
        warnings=backyard["warnings"],
        data_quality_score=min(100, quality),
    )
