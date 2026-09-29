from __future__ import annotations


def prioritize_habitation(habitation: dict, risk_result: dict) -> dict:
    score = (
        0.35 * risk_result["risk_score"]
        + 0.25 * habitation["population_vulnerability"] * 100
        + 0.20 * habitation["historical_impact"] * 100
        + 0.10 * habitation["population"] / 35
        + 0.10 * habitation["evacuation_difficulty"] * 100
    )

    if score >= 80:
        priority = "IMMEDIATE"
    elif score >= 65:
        priority = "SHORT-TERM"
    elif score >= 50:
        priority = "MEDIUM-TERM"
    else:
        priority = "MONITOR"

    reasons = [
        f"{risk_result['risk_class']} risk class",
        f"{habitation['population']} residents exposed",
        f"{habitation['historical_impact'] * 100:.0f}% historical impact intensity",
        f"{habitation['evacuation_difficulty'] * 100:.0f}% evacuation difficulty",
    ]

    return {
        "priority": priority,
        "score": round(score, 1),
        "reasons": reasons,
        "explanation": (
            f"{habitation['name']} is prioritized as {priority} because it combines high risk, repeated disaster impact, "
            f"a large exposed population, and difficulty evacuating residents safely."
        ),
    }
