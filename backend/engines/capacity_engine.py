from __future__ import annotations


def calculate_capacity(site: dict) -> dict:
    """Calculate effective carrying capacity using the minimum of infrastructure constraints."""
    capacities = {
        "Land Capacity": site["land_capacity"],
        "Water Capacity": site["water_capacity"],
        "Road Capacity": site["road_capacity"],
        "Healthcare Capacity": site["healthcare_capacity"],
        "School Capacity": site["school_capacity"],
        "Environmental Capacity": site["environmental_capacity"],
        "Shelter Capacity": site["shelter_capacity"],
    }
    effective_capacity = min(capacities.values())
    limiting_factor = min(capacities, key=capacities.get)

    return {
        "capacities": capacities,
        "effective_capacity": effective_capacity,
        "limiting_factor": limiting_factor,
        "explanation": (
            f"Site {site['name']} is limited by {limiting_factor.lower()} capacity in the prototype model."
        ),
    }
