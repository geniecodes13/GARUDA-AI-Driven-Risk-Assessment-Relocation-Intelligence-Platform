from __future__ import annotations

from backend.config import HAZARD_WEIGHTS


def calculate_hazard_score(habitation: dict) -> dict:
    """Compute the prototype hazard score and show per-factor contribution."""
    flood = habitation["flood_exposure"]
    landslide = habitation["landslide_exposure"]
    historical = habitation["historical_impact"]
    accessibility = habitation["accessibility_risk"]

    score = (
        HAZARD_WEIGHTS["flood"] * flood
        + HAZARD_WEIGHTS["landslide"] * landslide
        + HAZARD_WEIGHTS["historical"] * historical
    )

    contribution = {
        "Flood Exposure": round(flood * 100, 1),
        "Landslide Exposure": round(landslide * 100, 1),
        "Historical Disaster Impact": round(historical * 100, 1),
        "Accessibility Risk": round(accessibility * 100, 1),
    }

    return {
        "score": round(score, 4),
        "score_100": round(score * 100, 1),
        "components": contribution,
        "confidence": 0.82,
        "data_sources": ["Prototype hazard layer", "Disaster history log", "Accessibility proxy"],
        "data_freshness": "Prototype hazard layer (2025), local road/accessibility review (2026)",
    }
