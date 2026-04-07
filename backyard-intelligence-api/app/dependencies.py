"""Dependency providers for FastAPI routers."""

from app.config import settings
from app.providers.arcgis_provider import ArcGISProvider
from app.providers.county_gis_provider import CountyGISProvider
from app.providers.google_provider import GoogleGeocodingProvider
from app.providers.mapbox_provider import MapboxProvider
from app.providers.osm_provider import OSMProvider
from app.services.backyard_service import BackyardService
from app.services.building_service import BuildingService
from app.services.geocoding_service import GeocodingService
from app.services.imagery_service import ImageryService
from app.services.orientation_service import OrientationService
from app.services.parcel_service import ParcelService
from app.services.roads_service import RoadsService
from app.services.scoring_service import ScoringService

county_provider = CountyGISProvider()

def get_geocoding_service() -> GeocodingService:
    return GeocodingService(GoogleGeocodingProvider(settings.google_geocoding_api_key))


def get_imagery_service() -> ImageryService:
    return ImageryService(MapboxProvider(settings.mapbox_api_token), ArcGISProvider(settings.arcgis_api_key))


def get_parcel_service() -> ParcelService:
    return ParcelService(county_provider)


def get_building_service() -> BuildingService:
    return BuildingService(county_provider)


def get_roads_service() -> RoadsService:
    return RoadsService(OSMProvider())


def get_orientation_service() -> OrientationService:
    return OrientationService()


def get_backyard_service() -> BackyardService:
    return BackyardService()


def get_scoring_service() -> ScoringService:
    return ScoringService()
