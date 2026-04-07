"""LOVING service scoring business logic."""

from __future__ import annotations

from app.models.response_models import SalesRecommendation, ServiceScore

SERVICES = ["turf", "patio", "drainage", "lighting", "pergola", "outdoor_kitchen", "planting"]


class ScoringService:
    def _fit_label(self, score: int) -> str:
        if score >= 85:
            return "excellent"
        if score >= 70:
            return "good"
        if score >= 50:
            return "conditional"
        return "poor"

    def score_services(self, site_metrics: dict, requested: list[str] | None = None) -> dict[str, ServiceScore]:
        req = requested or SERVICES
        drainage_risk = site_metrics.get("drainage_risk", "medium")
        canopy_uncertain = site_metrics.get("canopy_interference_uncertain", True)

        results: dict[str, ServiceScore] = {}
        for service in req:
            reasons: list[str] = []
            score = 70
            onsite = False

            if service == "drainage":
                score = 90 if drainage_risk == "high" else 70
                reasons.append("Drainage baseline set from slope/water-flow uncertainty.")
                onsite = True
            elif service == "outdoor_kitchen":
                score = 60
                reasons.extend([
                    "Utility review required.",
                    "Setback and permit review required.",
                ])
                onsite = True
            elif service == "pergola":
                score = 65 if canopy_uncertain else 78
                reasons.append("Conditional due to possible canopy interference or unclear anchoring surface.")
                onsite = True
            elif service == "lighting":
                score = 80
                reasons.append("Cross-sell opportunity for path and entertainment zones.")
            elif service == "planting":
                score = 82 if drainage_risk != "high" else 68
                reasons.append("Planting usually flexible unless constraints are severe.")
            elif service == "patio":
                score = 74
                reasons.append("Good fit if drainage mitigation is planned where needed.")
            elif service == "turf":
                score = 72 if drainage_risk != "high" else 55
                reasons.append("Turf fit drops when drainage risk is high.")

            results[service] = ServiceScore(
                score=score,
                fit_label=self._fit_label(score),
                reasons=reasons,
                onsite_verification_required=onsite,
            )

        return results

    def sales_recommendation(self, service_scores: dict[str, ServiceScore], drainage_risk: str) -> SalesRecommendation:
        ranked = sorted(service_scores.items(), key=lambda x: x[1].score, reverse=True)
        best = [name for name, _ in ranked[:3]]
        do_not_quote = [name for name, score in ranked if score.onsite_verification_required]

        bundles = []
        if "lighting" in service_scores and "patio" in service_scores:
            bundles.append("Patio + Lighting Entertainment Bundle")
        if "planting" in service_scores and "lighting" in service_scores:
            bundles.append("Planting + Lighting Curb Appeal Bundle")
        if drainage_risk == "high":
            bundles.insert(0, "Drainage First Bundle before Turf/Hardscape")

        lead_quality = "high" if ranked and ranked[0][1].score >= 80 else "medium"
        visit_priority = "high" if drainage_risk == "high" or len(do_not_quote) > 1 else "medium"

        return SalesRecommendation(
            lead_quality=lead_quality,
            best_services_to_pitch_first=best,
            bundle_opportunities=bundles,
            do_not_quote_remotely=do_not_quote,
            onsite_visit_priority=visit_priority,
        )
