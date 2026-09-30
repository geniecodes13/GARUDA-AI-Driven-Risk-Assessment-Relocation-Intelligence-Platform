from __future__ import annotations

from math import asin, cos, radians, sin, sqrt


def calculate_distance_km(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> float:
    """Calculate great-circle distance between two coordinate pairs."""
    start_lat_rad, end_lat_rad = radians(start_lat), radians(end_lat)
    latitude_delta = end_lat_rad - start_lat_rad
    longitude_delta = radians(end_lon - start_lon)
    haversine = (
        sin(latitude_delta / 2) ** 2
        + cos(start_lat_rad) * cos(end_lat_rad) * sin(longitude_delta / 2) ** 2
    )
    return 6371.0088 * 2 * asin(sqrt(haversine))


def evaluate_site(site: dict, habitation: dict, max_distance_km: float = 35) -> dict:
    """Apply hard and soft constraints for relocation sites."""
    hard_fail = (
        site["flood_risk"] > 0.65
        or site["landslide_risk"] > 0.70
        or site["usable_land_sqkm"] < 1.2
        or site["distance_km"] > max_distance_km
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


def find_nearby_safe_sites(
    habitation: dict,
    sites: list[dict],
    max_distance_km: float = 35,
) -> list[dict]:
    nearby_safe_sites = []
    for site in sites:
        distance = calculate_distance_km(
            habitation["lat"], habitation["lon"], site["lat"], site["lon"]
        )
        located_site = {**site, "distance_km": distance}
        evaluation = evaluate_site(located_site, habitation, max_distance_km)
        if evaluation["status"] == "SAFE":
            nearby_safe_sites.append({**located_site, **evaluation})
    return nearby_safe_sites


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
