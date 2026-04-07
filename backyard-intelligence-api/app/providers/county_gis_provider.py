"""County GIS provider stub.

Replace this with county-specific connectors or vendor feeds.
"""

from __future__ import annotations

from shapely.geometry import Polygon


class CountyGISProvider:
    async def lookup_parcel(self, lat: float, lon: float) -> dict | None:
        # Stub: returns synthetic parcel around geocode point.
        d = 0.00015
        poly = Polygon([(lon - d, lat - d), (lon + d, lat - d), (lon + d, lat + d), (lon - d, lat + d)])
        return {
            "parcel_id": "stub-parcel-001",
            "jurisdiction": "stub-county",
            "lot_area_sqft": 7200,
            "zoning": None,
            "geometry": poly,
        }

    async def lookup_building(self, lat: float, lon: float) -> dict | None:
        d = 0.00006
        poly = Polygon([(lon - d, lat - d), (lon + d, lat - d), (lon + d, lat + d), (lon - d, lat + d)])
        return {"building_id": "stub-bldg-001", "geometry": poly, "building_area_sqft": 1800}
