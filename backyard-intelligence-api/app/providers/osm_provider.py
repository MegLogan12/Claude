"""OSM provider for nearby roads via Overpass API."""

from __future__ import annotations

import httpx
from shapely.geometry import LineString


class OSMProvider:
    async def nearest_road(self, lat: float, lon: float) -> LineString | None:
        query = f"""
        [out:json];
        way(around:80,{lat},{lon})["highway"];
        out geom 1;
        """
        async with httpx.AsyncClient(timeout=12) as client:
            resp = await client.post("https://overpass-api.de/api/interpreter", data=query)
            if resp.status_code >= 400:
                return None
            payload = resp.json()
            elements = payload.get("elements", [])
            for el in elements:
                geom = el.get("geometry")
                if geom and len(geom) >= 2:
                    coords = [(p["lon"], p["lat"]) for p in geom]
                    return LineString(coords)
            return None
