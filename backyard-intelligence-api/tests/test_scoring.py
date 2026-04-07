from app.services.scoring_service import ScoringService


def test_scoring_output_structure() -> None:
    service = ScoringService()
    scores = service.score_services({"drainage_risk": "high", "canopy_interference_uncertain": True})
    assert "outdoor_kitchen" in scores
    kitchen = scores["outdoor_kitchen"]
    assert kitchen.onsite_verification_required is True
    assert any("Utility review required" in r for r in kitchen.reasons)
