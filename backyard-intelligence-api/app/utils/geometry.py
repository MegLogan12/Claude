"""Geometry utility functions."""

from __future__ import annotations

from math import cos, radians
from typing import Any

from shapely import affinity
from shapely.geometry import LineString, Polygon, box, mapping


def sqft_from_polygon(poly: Polygon) -> float:
    """Approximate square feet from a lon/lat polygon near its centroid latitude."""
    centroid_lat = poly.centroid.y
    m_per_deg_lat = 111_132
    m_per_deg_lon = 111_320 * cos(radians(centroid_lat))
    scaled = affinity.scale(poly, xfact=m_per_deg_lon, yfact=m_per_deg_lat, origin=(0, 0))
    return scaled.area * 10.7639


def split_backyard_from_parcel(parcel: Polygon, front_direction: str = "south") -> Polygon:
    """Split parcel into halves and return opposite side to likely front."""
    minx, miny, maxx, maxy = parcel.bounds
    midx = (minx + maxx) / 2
    midy = (miny + maxy) / 2

    if front_direction == "north":
        candidate = box(minx, miny, maxx, midy)
    elif front_direction == "south":
        candidate = box(minx, midy, maxx, maxy)
    elif front_direction == "east":
        candidate = box(minx, miny, midx, maxy)
    else:
        candidate = box(midx, miny, maxx, maxy)

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
