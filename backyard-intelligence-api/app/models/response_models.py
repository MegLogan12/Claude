"""Response models."""

from typing import Any, Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class GeocodeOut(BaseModel):
    latitude: float
    longitude: float
    place_id: str | None = None


class ServiceScore(BaseModel):
    score: int
    fit_label: Literal["poor", "conditional", "good", "excellent"]
    reasons: list[str]
    onsite_verification_required: bool


class SalesRecommendation(BaseModel):
    lead_quality: Literal["low", "medium", "high"]
    best_services_to_pitch_first: list[str]
    bundle_opportunities: list[str]
    do_not_quote_remotely: list[str]
    onsite_visit_priority: Literal["low", "medium", "high"]


class BackyardPolygonResponse(BaseModel):
    backyard_found: bool
    confidence: Literal["low", "medium", "high"]
    method_used: str
    backyard_polygon_geojson: dict[str, Any] | None
    estimated_backyard_area_sqft: float | None
    front_yard_direction: str | None
    fallback_used: bool
    warnings: list[str]


class BackyardImageResponse(BaseModel):
    input_address: str
    normalized_address: str
    geocode: GeocodeOut
    parcel_summary: dict[str, Any] | None
    building_summary: dict[str, Any] | None
    backyard_centroid: dict[str, float] | None
    backyard_confidence: Literal["low", "medium", "high"]
    imagery_provider: str
    imagery_url: str
    fallback_used: bool
    warnings: list[str]
    data_quality_score: int
