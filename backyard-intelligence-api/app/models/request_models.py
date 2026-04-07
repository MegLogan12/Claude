"""Request models."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.utils.validation import is_valid_us_address


class AddressRequest(BaseModel):
    """Base request with US address validation."""

    address: str = Field(..., description="US street address in 'street, city, ST ZIP' format")

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str) -> str:
        if not is_valid_us_address(value):
            raise ValueError("Address must be a US address in format '123 Main St, City, ST 12345'")
        return value


class BackyardImageRequest(AddressRequest):
    imagery_provider: Literal["arcgis", "mapbox"] = "arcgis"
    zoom: int = Field(default=20, ge=15, le=22)
    width: int = Field(default=640, ge=256, le=1280)
    height: int = Field(default=640, ge=256, le=1280)


class PropertyAnalyzeRequest(AddressRequest):
    requested_services: list[
        Literal["turf", "patio", "drainage", "lighting", "pergola", "outdoor_kitchen", "planting"]
    ] = Field(default_factory=list)
