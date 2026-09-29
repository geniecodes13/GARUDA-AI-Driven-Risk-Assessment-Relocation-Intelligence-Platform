"""Configuration values for the GARUDA MVP prototype."""

HAZARD_WEIGHTS = {
    "flood": 0.40,
    "landslide": 0.35,
    "historical": 0.25,
}

VULNERABILITY_WEIGHTS = {
    "population": 0.30,
    "housing": 0.20,
    "healthcare": 0.20,
    "road": 0.15,
    "evacuation": 0.15,
}

RISK_THRESHOLDS = [20, 40, 60, 80]
RISK_LABELS = ["Low", "Moderate", "High", "Very High", "Critical"]
PRIORITY_LABELS = ["MONITOR", "MEDIUM-TERM", "SHORT-TERM", "IMMEDIATE"]

SITE_HARD_CONSTRAINTS = {
    "max_flood_risk": 0.65,
    "max_landslide_risk": 0.70,
    "min_usable_land": 600,
    "max_distance_km": 35,
}

RESOURCE_STANDARDS = {
    "water_per_person": 0.020,
    "food_per_person": 0.060,
    "shelter_per_person": 0.060,
    "medical_per_person": 0.010,
    "transport_per_person": 0.004,
}
