from __future__ import annotations


def evaluate_site(site: dict, habitation: dict) -> dict:
    """Apply hard and soft constraints for relocation sites."""
    hard_fail = (
        site["flood_risk"] > 0.65
        or site["landslide_risk"] > 0.70
        or site["usable_land_sqkm"] < 1.2
        or site["distance_km"] > 35
    )

    if hard_fail:
        return {
            "status": "REJECTED",
            "reason": "Hard constraints failed: flood risk, landslide risk, land availability, or access threshold exceeded.",
            "suitability_score": 0,
        }

    soft_score = (
        0.30 * (1 - site["flood_risk"]) +
        0.25 * (1 - site["landslide_risk"]) +
        0.20 * (1 / (1 + site["distance_km"] / 10)) +
        0.15 * min(1.0, site["water_capacity"] / 2000) +
        0.10 * min(1.0, site["healthcare_capacity"] / 1800)
    )

    return {
        "status": "SAFE",
        "reason": "Site passes hard constraints and remains viable under soft suitability criteria.",
        "suitability_score": round(soft_score, 3),
    }


def build_candidate_sites(habitations: list, sites: list) -> list:
    results = []
    for h in habitations:
        site_list = []
        for site in sites:
            match = evaluate_site(site, h)
            site_info = {**site, **match}
            site_list.append(site_info)
        results.append({"habitation": h["name"], "sites": site_list})
    return results
