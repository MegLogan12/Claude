"""Analysis router."""

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_backyard_service,
    get_building_service,
    get_geocoding_service,
    get_orientation_service,
    get_parcel_service,
    get_roads_service,
    get_scoring_service,
)
from app.models.request_models import AddressRequest, PropertyAnalyzeRequest
from app.models.response_models import BackyardPolygonResponse
from app.services.backyard_service import BackyardService
from app.services.building_service import BuildingService
from app.services.geocoding_service import GeocodingService
from app.services.orientation_service import OrientationService
from app.services.parcel_service import ParcelService
from app.services.roads_service import RoadsService
from app.services.scoring_service import ScoringService

router = APIRouter(prefix="/v1", tags=["analysis"])


@router.post("/backyard-polygon", response_model=BackyardPolygonResponse)
async def backyard_polygon(
    req: AddressRequest,
    geocoder: GeocodingService = Depends(get_geocoding_service),
    parcel_service: ParcelService = Depends(get_parcel_service),
    building_service: BuildingService = Depends(get_building_service),
    roads_service: RoadsService = Depends(get_roads_service),
    orientation_service: OrientationService = Depends(get_orientation_service),
    backyard_service: BackyardService = Depends(get_backyard_service),
) -> BackyardPolygonResponse:
    geocode = await geocoder.geocode(req.address)
    parcel = await parcel_service.lookup(geocode["latitude"], geocode["longitude"])
    building = await building_service.lookup(geocode["latitude"], geocode["longitude"])
    road = await roads_service.nearest_road(geocode["latitude"], geocode["longitude"])
    front = orientation_service.infer_front_direction(parcel["geometry"], road) if parcel else None
    result = backyard_service.infer_backyard(geocode["latitude"], geocode["longitude"], parcel, building, front)
    return BackyardPolygonResponse(**{k: result[k] for k in BackyardPolygonResponse.model_fields})


@router.post("/property-analyze")
async def property_analyze(
    req: PropertyAnalyzeRequest,
    geocoder: GeocodingService = Depends(get_geocoding_service),
    parcel_service: ParcelService = Depends(get_parcel_service),
    building_service: BuildingService = Depends(get_building_service),
    roads_service: RoadsService = Depends(get_roads_service),
    orientation_service: OrientationService = Depends(get_orientation_service),
    backyard_service: BackyardService = Depends(get_backyard_service),
    scoring_service: ScoringService = Depends(get_scoring_service),
) -> dict:
    geocode = await geocoder.geocode(req.address)
    parcel = await parcel_service.lookup(geocode["latitude"], geocode["longitude"])
    building = await building_service.lookup(geocode["latitude"], geocode["longitude"])
    road = await roads_service.nearest_road(geocode["latitude"], geocode["longitude"])

    warnings: list[str] = []
    if not parcel:
        warnings.append("Parcel unavailable; analysis confidence reduced.")
    if not road:
        warnings.append("Road geometry unavailable; front/back orientation less certain.")

    front = orientation_service.infer_front_direction(parcel["geometry"], road) if parcel else None
    backyard = backyard_service.infer_backyard(geocode["latitude"], geocode["longitude"], parcel, building, front)

    drainage_risk = "high" if backyard["confidence"] == "low" else "medium"
    site_metrics = {
        "backyard_area_sqft": backyard["estimated_backyard_area_sqft"],
        "drainage_risk": drainage_risk,
        "canopy_interference_uncertain": True,
        "access_constraints": "unknown",
    }
    service_scores = scoring_service.score_services(site_metrics, req.requested_services)
    sales = scoring_service.sales_recommendation(service_scores, drainage_risk)

    next_actions = ["Schedule onsite verification for utilities, drainage, and setbacks."]
    if drainage_risk == "high":
        next_actions.insert(0, "Perform drainage evaluation before finalizing hardscape or turf.")

    quality = 40
    if parcel:
        quality += 30
    if building:
        quality += 20
    if road:
        quality += 10

    return {
        "overall_summary": "Remote property analysis generated from aerial and GIS-derived signals.",
        "site_metrics": site_metrics,
        "service_scores": {k: v.model_dump() for k, v in service_scores.items()},
        "best_services_to_pitch_first": sales.best_services_to_pitch_first,
        "bundle_opportunities": sales.bundle_opportunities,
        "do_not_quote_remotely": sales.do_not_quote_remotely,
        "onsite_verification_requirements": [
            "Utility locates",
            "Setback and permit checks",
            "Drainage slope confirmation",
        ],
        "sales_recommendation": sales.model_dump(),
        "warnings": warnings + backyard["warnings"],
        "fallback_used": backyard["fallback_used"],
        "data_quality_score": min(100, quality),
        "next_best_actions": next_actions,
    }
