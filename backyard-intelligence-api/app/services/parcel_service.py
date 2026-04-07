"""Parcel lookup service."""

from app.providers.county_gis_provider import CountyGISProvider


class ParcelService:
    def __init__(self, county_provider: CountyGISProvider) -> None:
        self.county_provider = county_provider

    async def lookup(self, lat: float, lon: float) -> dict | None:
        return await self.county_provider.lookup_parcel(lat, lon)
