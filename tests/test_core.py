from backend.data.demo_data import CANDIDATE_SITES, HABITATIONS
from backend.data.census_data import find_census_subdistrict, load_census_subdistricts
from backend.data.realtime_data import parse_district_rainfall
from backend.engines.capacity_engine import calculate_capacity
from backend.engines.hazard_engine import calculate_hazard_score
from backend.engines.priority_engine import prioritize_habitation
from backend.engines.risk_engine import compute_risk, classify_risk
from backend.engines.simulation_engine import run_scenario
from backend.engines.site_engine import calculate_distance_km, evaluate_site, find_nearby_safe_sites
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


def test_imd_district_rainfall_parser():
    page = '''
    {"title": "DEHRADUN", "id": "544", "color": "#fff",
     "balloonText": "<h6>DEHRADUN</h6><p>Date : 2026-09-29</br>Departure : 102%</br>Actual : 5.4 mm</br>Normal : 2.7 mm</p>"}
    {"title": "NAGAPATTINAM", "id": "000", "color": "#fff",
     "balloonText": "<h6>NAGAPATTINAM</h6><p>Date : 0000-00-00</br>Departure : -100%</br>Actual : 0 mm</br>Normal : 1 mm</p>"}
    '''

    result = parse_district_rainfall(page)

    assert result == [{
        "district": "DEHRADUN",
        "report_date": "2026-09-29",
        "actual_mm": 5.4,
        "normal_mm": 2.7,
        "departure_percent": 102.0,
    }]


def test_census_2011_subdistrict_population_mapping():
    census = load_census_subdistricts()

    bhatwari = find_census_subdistrict("Uttarkashi", "Bhatwari", census)
    assert bhatwari["population"] == 75056
    assert bhatwari["district_code"] == "056"
    assert bhatwari["subdistrict_code"] == "00283"
    assert find_census_subdistrict("Rudraprayag", "Kalimath", census) is None


def test_relocation_scenario_uses_effective_safe_site_capacity():
    site = dict(CANDIDATE_SITES[0])
    site["status"] = "SAFE"
    site["land_capacity"] = 10000
    site["water_capacity"] = 400

    result = run_scenario(1000, 60, [site])

    assert result["capacity_available"] == 400
    assert result["relocated"] == 600
    assert result["capacity_gap"] == 200


def test_site_distance_uses_haversine_coordinates():
    assert calculate_distance_km(30.0, 79.0, 30.0, 79.0) == 0
    assert 111 < calculate_distance_km(0.0, 0.0, 0.0, 1.0) < 112


def test_site_max_distance_can_be_set_for_local_discovery():
    site = dict(CANDIDATE_SITES[0], distance_km=40)

    assert evaluate_site(site, HABITATIONS[0])["status"] == "REJECTED"
    assert evaluate_site(site, HABITATIONS[0], max_distance_km=45)["status"] == "SAFE"


def test_nearby_discovery_and_scenario_share_same_safe_sites():
    nearby_sites = find_nearby_safe_sites(HABITATIONS[0], CANDIDATE_SITES, 35)
    scenario = run_scenario(75056, 60, nearby_sites)

    assert [site["name"] for site in nearby_sites] == ["Chataun Basin"]
    assert scenario["capacity_available"] == sum(
        calculate_capacity(site)["effective_capacity"] for site in nearby_sites
    )
