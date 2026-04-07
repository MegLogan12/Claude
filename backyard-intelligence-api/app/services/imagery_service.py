"""Imagery URL generation service."""

from app.providers.arcgis_provider import ArcGISProvider
from app.providers.mapbox_provider import MapboxProvider


class ImageryService:
    def __init__(self, mapbox: MapboxProvider, arcgis: ArcGISProvider) -> None:
        self.mapbox = mapbox
        self.arcgis = arcgis

    def imagery_url(self, provider: str, lat: float, lon: float, zoom: int, width: int, height: int) -> str:
        if provider == "mapbox":
            return self.mapbox.static_imagery_url(lat=lat, lon=lon, zoom=zoom, width=width, height=height)
        return self.arcgis.static_imagery_url(lat=lat, lon=lon, zoom=zoom, width=width, height=height)
