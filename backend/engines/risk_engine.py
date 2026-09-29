from __future__ import annotations

from backend.config import RISK_THRESHOLDS


def classify_risk(score_100: float) -> str:
    if score_100 < RISK_THRESHOLDS[0]:
        return "Low"
    if score_100 < RISK_THRESHOLDS[1]:
        return "Moderate"
    if score_100 < RISK_THRESHOLDS[2]:
        return "High"
    if score_100 < RISK_THRESHOLDS[3]:
        return "Very High"
    return "Critical"


def compute_risk(habitation: dict, hazard_result: dict, vulnerability_result: dict) -> dict:
    risk_score = hazard_result["score"] * vulnerability_result["score"]
    risk_100 = risk_score * 100
    risk_class = classify_risk(risk_100)
    return {
        "risk_score": round(risk_100, 1),
        "risk_class": risk_class,
        "confidence": 0.81,
        "major_factors": [
            "Hazard exposure",
            "Population vulnerability",
            "Limited evacuation connectivity",
        ],
        "data_freshness": {
            "population": "2011 Census baseline",
            "hazard": "2025 prototype layer",
            "roads": "2026 review",
        },
        "data_sources": ["Hazard layer", "Population proxy", "Road network review"],
        "risk_formula": "Hazard Exposure × Vulnerability",
        "drivers": {
            "hazard_contribution": round(hazard_result["score_100"] / 100, 4),
            "vulnerability_contribution": round(vulnerability_result["score_100"] / 100, 4),
        },
        "explanation": (
            "AI-assessed high-risk zone — prototype score based on hazard exposure and vulnerability; "
            "this is not a legal Red Zone declaration."
        ),
    }
