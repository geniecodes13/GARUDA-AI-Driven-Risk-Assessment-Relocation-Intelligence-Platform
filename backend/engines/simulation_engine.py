from __future__ import annotations


def run_scenario(population, percentage_to_relocate, sites, resources=None):
    """Compute the what-if relocation scenario and show capacity gap."""
    relocated = int(population * max(0, min(1, percentage_to_relocate / 100)))
    safe_sites = [site for site in sites if site["status"] == "SAFE"]
    total_capacity = sum(site["land_capacity"] for site in safe_sites)
    capacity_gap = max(0, relocated - total_capacity)
    resource_gap = 0
    if resources:
        resource_gap = sum(max(0, item["deployed_quantity"] - item["available_quantity"]) for item in resources)

    return {
        "population": population,
        "percentage": percentage_to_relocate,
        "relocated": relocated,
        "capacity_available": total_capacity,
        "capacity_gap": capacity_gap,
        "resource_gap": resource_gap,
        "scenario_summary": (
            f"Relocating {percentage_to_relocate}% means {relocated} residents; the demonstration set offers "
            f"{total_capacity} people of site capacity, leaving a gap of {capacity_gap} if the site network remains static."
        ),
    }
