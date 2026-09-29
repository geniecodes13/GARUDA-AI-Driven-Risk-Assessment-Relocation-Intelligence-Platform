from backend.data.demo_data import CANDIDATE_SITES, HABITATIONS
from backend.engines.capacity_engine import calculate_capacity
from backend.engines.hazard_engine import calculate_hazard_score
from backend.engines.priority_engine import prioritize_habitation
from backend.engines.risk_engine import compute_risk, classify_risk
from backend.engines.site_engine import evaluate_site
from backend.engines.vulnerability_engine import calculate_vulnerability_score


def test_hazard_score_range():
    result = calculate_hazard_score(HABITATIONS[0])
    assert 0 <= result["score"] <= 1


def test_vulnerability_score_range():
    result = calculate_vulnerability_score(HABITATIONS[0])
    assert 0 <= result["score"] <= 1


def test_risk_classification_bounds():
    assert classify_risk(10) == "Low"
    assert classify_risk(25) == "Moderate"
    assert classify_risk(45) == "High"
    assert classify_risk(75) == "Very High"
    assert classify_risk(95) == "Critical"


def test_capacity_is_minimum_of_constraints():
    site = CANDIDATE_SITES[0]
    result = calculate_capacity(site)
    expected = min(site["land_capacity"], site["water_capacity"], site["road_capacity"], site["healthcare_capacity"], site["school_capacity"], site["environmental_capacity"], site["shelter_capacity"])
    assert result["effective_capacity"] == expected


def test_candidate_site_filter_rejects_high_risk_site():
    site = CANDIDATE_SITES[-1]
    result = evaluate_site(site, HABITATIONS[0])
    assert result["status"] == "REJECTED"


def test_priority_is_returned_for_habitation():
    hazard = calculate_hazard_score(HABITATIONS[0])
    vulnerability = calculate_vulnerability_score(HABITATIONS[0])
    risk = compute_risk(HABITATIONS[0], hazard, vulnerability)
    result = prioritize_habitation(HABITATIONS[0], risk)
    assert result["priority"] in {"IMMEDIATE", "SHORT-TERM", "MEDIUM-TERM", "MONITOR"}
