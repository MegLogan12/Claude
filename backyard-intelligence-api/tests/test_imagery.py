from app.providers.arcgis_provider import ArcGISProvider
from app.providers.mapbox_provider import MapboxProvider


def test_imagery_url_generation() -> None:
    mapbox = MapboxProvider("token")
    arcgis = ArcGISProvider("")
    assert "mapbox.com" in mapbox.static_imagery_url(32.7, -96.8, 20, 640, 640)
    assert "arcgisonline.com" in arcgis.static_imagery_url(32.7, -96.8, 20, 640, 640)
