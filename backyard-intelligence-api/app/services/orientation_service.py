"""Front/back orientation inference service."""

from shapely.geometry import LineString, Polygon

from app.utils.geometry import guess_front_from_road


class OrientationService:
    def infer_front_direction(self, parcel: Polygon, road: LineString | None) -> str:
        return guess_front_from_road(parcel, road)
