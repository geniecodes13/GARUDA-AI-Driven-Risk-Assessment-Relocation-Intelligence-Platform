from __future__ import annotations

import re


def answer_question(question: str, habitations: list, sites: list, resources: list) -> dict:
    q = question.lower()
    if "show villages with very high risk" in q or "very high risk" in q:
        rows = [h for h in habitations if h["population"] > 2000 and (h["flood_exposure"] + h["landslide_exposure"]) / 2 > 0.7]
        return {"answer": rows[:5], "type": "risk_filter"}

    if "why is" in q and "prioritized" in q:
        top = sorted(habitations, key=lambda h: ((h["flood_exposure"] + h["landslide_exposure"]) / 2 + h["historical_impact"]) * 100, reverse=True)[0]
        return {
            "answer": {
                "habitation": top["name"],
                "reason": f"High multi-hazard exposure, repeated historical impacts, and elevated evacuation difficulty drive its priority.",
            },
            "type": "explanation",
        }

    if "largest population" in q and "site" in q:
        site = max(sites, key=lambda s: s["land_capacity"])
        return {"answer": {"site": site["name"], "capacity": site["land_capacity"]}, "type": "site_capacity"}

    if "limiting" in q and "capacity" in q:
        target = [site for site in sites if "site" in q or site["name"].lower() in q]
        if target:
            site = target[0]
            capacity = min(site["land_capacity"], site["water_capacity"], site["road_capacity"], site["healthcare_capacity"], site["school_capacity"], site["environmental_capacity"], site["shelter_capacity"])
            return {"answer": {"site": site["name"], "limiting_factor": "Water Capacity" if site["water_capacity"] == capacity else "Land Capacity", "capacity": capacity}, "type": "limiting_factor"}

    if "relocate" in q and "70" in q:
        percentage = 70
        safe_sites = [site for site in sites if site["status"] == "SAFE"]
        total_capacity = sum(site["land_capacity"] for site in safe_sites)
        relocated = 0
        for h in habitations:
            relocated += h["population"]
        return {
            "answer": {
                "population_relocated": int(relocated * 0.7),
                "capacity_available": total_capacity,
                "outcome": "Feasible" if total_capacity >= int(relocated * 0.7) else "Capacity gap remains",
            },
            "type": "scenario",
        }

    if "ambulances" in q and "available" in q:
        resource = next((r for r in resources if r["name"].lower() == "ambulance"), None)
        return {"answer": resource if resource else {"count": 0}, "type": "resource_query"}

    if "resource shortages" in q or "limiting relocation" in q:
        shortages = [r for r in resources if r["available_quantity"] < 0.6 * r["total_quantity"]]
        return {"answer": shortages, "type": "resource_shortages"}

    return {"answer": "The demonstration query is supported by structured GIS and resource logic. Please ask about risk, site capacity, or resource sufficiency.", "type": "generic"}
