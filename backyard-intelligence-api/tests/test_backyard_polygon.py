from shapely.geometry import Polygon

from app.services.backyard_service import BackyardService


def test_backyard_polygon_output_shape() -> None:
    service = BackyardService()
    parcel = {"geometry": Polygon([(-96.8, 32.7), (-96.79, 32.7), (-96.79, 32.71), (-96.8, 32.71)])}
    result = service.infer_backyard(32.705, -96.795, parcel, building={"ok": True}, front_direction="south")
    assert result["backyard_polygon_geojson"]["type"] == "Polygon"
    assert result["estimated_backyard_area_sqft"] > 0


def test_low_confidence_fallback_flow() -> None:
    service = BackyardService()
    result = service.infer_backyard(32.705, -96.795, parcel=None, building=None, front_direction=None)
    assert result["confidence"] == "low"
    assert result["fallback_used"] is True
