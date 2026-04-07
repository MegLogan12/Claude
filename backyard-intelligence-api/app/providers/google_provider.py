"""Google Geocoding provider client."""

from __future__ import annotations

import httpx


class GoogleGeocodingProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def geocode(self, address: str) -> dict:
        if not self.api_key:
            # deterministic fallback for local/dev testing
            return {
                "normalized_address": address.title(),
                "latitude": 32.7767,
                "longitude": -96.7970,
                "place_id": "stub-place-id",
                "provider": "stub",
            }

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={"address": address, "key": self.api_key},
            )
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("status") != "OK" or not payload.get("results"):
                raise ValueError(f"Google geocoding failed: {payload.get('status')}")
            top = payload["results"][0]
            return {
                "normalized_address": top["formatted_address"],
                "latitude": top["geometry"]["location"]["lat"],
                "longitude": top["geometry"]["location"]["lng"],
                "place_id": top.get("place_id"),
                "provider": "google",
            }
