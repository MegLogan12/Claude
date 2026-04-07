"""ArcGIS imagery provider."""


class ArcGISProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def static_imagery_url(self, lat: float, lon: float, zoom: int, width: int, height: int) -> str:
        # ArcGIS World_Imagery export endpoint.
        scale = 591657528 / (2 ** zoom)
        bbox = f"{lon-0.001},{lat-0.001},{lon+0.001},{lat+0.001}"
        return (
            "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
            f"?bbox={bbox}&bboxSR=4326&imageSR=4326&size={width},{height}&format=jpg&f=image&dpi=96&mapScale={scale:.0f}"
        )
