"""Road lookup service."""

from shapely.geometry import LineString

from app.providers.osm_provider import OSMProvider


class RoadsService:
    def __init__(self, osm_provider: OSMProvider) -> None:
        self.osm_provider = osm_provider

    async def nearest_road(self, lat: float, lon: float) -> LineString | None:
        return await self.osm_provider.nearest_road(lat, lon)
