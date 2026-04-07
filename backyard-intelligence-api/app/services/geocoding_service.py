"""Geocoding service."""

from app.providers.google_provider import GoogleGeocodingProvider


class GeocodingService:
    def __init__(self, provider: GoogleGeocodingProvider) -> None:
        self.provider = provider

    async def geocode(self, address: str) -> dict:
        return await self.provider.geocode(address)
