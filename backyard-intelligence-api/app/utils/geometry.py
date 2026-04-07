"""Geometry utility functions."""

from __future__ import annotations

from math import cos, radians
from typing import Any

from shapely import affinity
from shapely.geometry import LineString, Polygon, mapping


def sqft_from_polygon(poly: Polygon) -> float:
    """Approximate square feet from lon/lat polygon near centroid latitude."""
    centroid_lat = poly.centroid.y
    m_per_deg_lat = 111_132
    m_per_deg_lon = 111_320 * cos(radians(centroid_lat))
    scaled = affinity.scale(poly, xfact=m_per_deg_lon, yfact=m_per_deg_lat, origin=(0, 0))
    return scaled.area * 10.7639


def split_backyard_from_parcel(parcel: Polygon, front_direction: str = "south") -> Polygon:
    """Split parcel in half and return opposite side as backyard."""
    minx, miny, maxx, maxy = parcel.bounds
    if front_direction in {"north", "south"}:
        midy = (miny + maxy) / 2
        return Polygon([
            (minx, midy),
            (maxx, midy),
            (maxx, maxy if front_direction == "south" else midy),
            (minx, maxy if front_direction == "south" else midy),
        ]).intersection(parcel) if front_direction == "south" else Polygon([
            (minx, miny),
            (maxx, miny),
            (maxx, midy),
            (minx, midy),
        ]).intersection(parcel)
    midx = (minx + maxx) / 2
    if front_direction == "west":
        candidate = Polygon([(midx, miny), (maxx, miny), (maxx, maxy), (midx, maxy)])
    else:
        candidate = Polygon([(minx, miny), (midx, miny), (midx, maxy), (minx, maxy)])
    return candidate.intersection(parcel)


def guess_front_from_road(parcel: Polygon, road: LineString | None) -> str:
    """Guess front yard orientation by nearest parcel edge to road."""
    if road is None:
        return "south"
    minx, miny, maxx, maxy = parcel.bounds
    edges: dict[str, LineString] = {
        "north": LineString([(minx, maxy), (maxx, maxy)]),
        "south": LineString([(minx, miny), (maxx, miny)]),
        "east": LineString([(maxx, miny), (maxx, maxy)]),
        "west": LineString([(minx, miny), (minx, maxy)]),
    }
    return min(edges.items(), key=lambda item: item[1].distance(road))[0]


def polygon_geojson(poly: Polygon) -> dict[str, Any]:
    """GeoJSON mapping for a polygon."""
    return mapping(poly)
