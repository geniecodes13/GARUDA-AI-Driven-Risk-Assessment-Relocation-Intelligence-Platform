from __future__ import annotations

from backend.config import RESOURCE_STANDARDS


def estimate_resource_requirements(population_to_relocate: int) -> dict:
    return {
        "Water Requirement": round(population_to_relocate * RESOURCE_STANDARDS["water_per_person"], 2),
        "Food Packages": round(population_to_relocate * RESOURCE_STANDARDS["food_per_person"], 2),
        "Shelter Units": round(population_to_relocate * RESOURCE_STANDARDS["shelter_per_person"], 2),
        "Medical Kits": round(population_to_relocate * RESOURCE_STANDARDS["medical_per_person"], 2),
        "Transport Vehicles": round(population_to_relocate * RESOURCE_STANDARDS["transport_per_person"], 2),
    }


def assess_resource_sufficiency(requirements: dict, inventory: list) -> dict:
    rows = []
    for record in inventory:
        if record["name"] in {"Ambulance", "Rescue Vehicle", "Water Tanker", "Temporary Shelter", "Medical Kit", "Food Supplies"}:
            required = requirements.get(record["name"].replace(" ", " ") or "Water Requirement", 0)
            available = record["available_quantity"]
            deficit = max(0, required - available)
            rows.append({
                "resource": record["name"],
                "required": required,
                "available": available,
                "deficit": deficit,
                "status": "OK" if deficit == 0 else "WARN",
            })
    return {"rows": rows}


def compute_resource_readiness(resources: list) -> dict:
    total = sum(item["available_quantity"] for item in resources)
    total_capacity = sum(item["total_quantity"] for item in resources)
    readiness = round((total / total_capacity) * 100, 1) if total_capacity else 0
    return {
        "resource_readiness_percent": readiness,
        "critical_shortages": sum(1 for item in resources if item["available_quantity"] < 0.5 * item["total_quantity"]),
    }
