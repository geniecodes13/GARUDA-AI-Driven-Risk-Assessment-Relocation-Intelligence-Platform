from fastapi import FastAPI

from backend.data.demo_data import HABITATIONS, CANDIDATE_SITES, RESOURCE_INVENTORY
from backend.engines.capacity_engine import calculate_capacity
from backend.engines.hazard_engine import calculate_hazard_score
from backend.engines.priority_engine import prioritize_habitation
from backend.engines.risk_engine import compute_risk
from backend.engines.vulnerability_engine import calculate_vulnerability_score

app = FastAPI(title="GARUDA Relocation Intelligence API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "GARUDA"}


@app.get("/api/v1/risk-summary")
def risk_summary():
    rows = []
    for habitation in HABITATIONS:
        hazard = calculate_hazard_score(habitation)
        vuln = calculate_vulnerability_score(habitation)
        risk = compute_risk(habitation, hazard, vuln)
        priority = prioritize_habitation(habitation, risk)
        rows.append({
            "name": habitation["name"],
            "population": habitation["population"],
            "risk_score": risk["risk_score"],
            "risk_class": risk["risk_class"],
            "priority": priority["priority"],
        })
    return rows


@app.get("/api/v1/sites")
def list_sites():
    site_rows = []
    for site in CANDIDATE_SITES:
        site_rows.append({"name": site["name"], "status": site["status"], **calculate_capacity(site)})
    return site_rows


@app.get("/api/v1/resources")
def list_resources():
    return RESOURCE_INVENTORY


@app.get("/api/v1/habitations")
def list_habitations():
    return HABITATIONS
