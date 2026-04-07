"""Mapbox imagery provider."""


class MapboxProvider:
    def __init__(self, token: str) -> None:
        self.token = token

    def static_imagery_url(self, lat: float, lon: float, zoom: int, width: int, height: int) -> str:
        base = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static"
        return f"{base}/{lon},{lat},{zoom},0/{width}x{height}?access_token={self.token or 'demo-token'}"
