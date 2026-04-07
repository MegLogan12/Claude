"""Backyard inference service."""

from __future__ import annotations

from shapely.geometry import Point, Polygon

from app.utils.geometry import polygon_geojson, split_backyard_from_parcel, sqft_from_polygon


class BackyardService:
    def infer_backyard(
        self,
        lat: float,
        lon: float,
        parcel: dict | None,
        building: dict | None,
        front_direction: str | None,
    ) -> dict:
        warnings: list[str] = []
        fallback_used = False

        if parcel and isinstance(parcel.get("geometry"), Polygon):
            front = front_direction or "south"
            backyard_poly = split_backyard_from_parcel(parcel["geometry"], front)
            confidence = "high" if building else "medium"
            if not building:
                warnings.append("Building footprint unavailable; backyard split is parcel-only estimate.")
            return {
                "backyard_found": True,
                "confidence": confidence,
                "method_used": "parcel_split_with_road_orientation",
                "backyard_polygon_geojson": polygon_geojson(backyard_poly),
                "estimated_backyard_area_sqft": round(sqft_from_polygon(backyard_poly), 1),
                "front_yard_direction": front,
                "fallback_used": fallback_used,
                "warnings": warnings,
                "centroid": {"latitude": backyard_poly.centroid.y, "longitude": backyard_poly.centroid.x},
            }

        fallback_used = True
        warnings.append("Parcel geometry unavailable; used geocode heuristic offset for backyard estimate.")
        p = Point(lon, lat - 0.00008)
        d = 0.00005
        fallback_poly = Polygon([(p.x - d, p.y - d), (p.x + d, p.y - d), (p.x + d, p.y + d), (p.x - d, p.y + d)])
        return {
            "backyard_found": True,
            "confidence": "low",
            "method_used": "geocode_offset_fallback",
            "backyard_polygon_geojson": polygon_geojson(fallback_poly),
            "estimated_backyard_area_sqft": round(sqft_from_polygon(fallback_poly), 1),
            "front_yard_direction": None,
            "fallback_used": fallback_used,
            "warnings": warnings,
            "centroid": {"latitude": fallback_poly.centroid.y, "longitude": fallback_poly.centroid.x},
        }
