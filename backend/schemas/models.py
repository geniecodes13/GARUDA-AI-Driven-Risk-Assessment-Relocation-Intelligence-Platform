from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class Habitat(BaseModel):
    id: str
    name: str
    district: str
    block: str
    state: str = "Uttarakhand"
    population: int
    lat: float
    lon: float
    flood_exposure: float = Field(ge=0, le=1)
    landslide_exposure: float = Field(ge=0, le=1)
    historical_impact: float = Field(ge=0, le=1)
    accessibility_risk: float = Field(ge=0, le=1)
    population_vulnerability: float = Field(ge=0, le=1)
    housing_vulnerability: float = Field(ge=0, le=1)
    healthcare_accessibility_risk: float = Field(ge=0, le=1)
    road_accessibility_risk: float = Field(ge=0, le=1)
    evacuation_difficulty: float = Field(ge=0, le=1)
    critical_infrastructure_risk: float = Field(ge=0, le=1)
    disaster_history: int = 0
    infrastructure_note: str = ""


class CandidateSite(BaseModel):
    id: str
    name: str
    district: str
    lat: float
    lon: float
    status: str = "SAFE"
    distance_km: float = 0
    flood_risk: float = Field(ge=0, le=1)
    landslide_risk: float = Field(ge=0, le=1)
    usable_land_sqkm: float = 0
    land_capacity: int = 0
    water_capacity: int = 0
    road_capacity: int = 0
    healthcare_capacity: int = 0
    school_capacity: int = 0
    environmental_capacity: int = 0
    shelter_capacity: int = 0
    infrastructure_gap: str = ""


class ResourceRecord(BaseModel):
    id: str
    name: str
    category: str
    location: str
    total_quantity: int
    available_quantity: int
    deployed_quantity: int
    status: str
    last_updated: str
    notes: Optional[str] = None


class Explanation(BaseModel):
    decision: str
    score: float
    confidence: float
    drivers: List[dict]
    data_sources: List[str]
    data_freshness: dict
