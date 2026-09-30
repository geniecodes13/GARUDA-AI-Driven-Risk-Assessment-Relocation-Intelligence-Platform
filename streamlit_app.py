from __future__ import annotations

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

from backend.ai_assistant import answer_question
from backend.data.census_data import find_census_subdistrict, load_census_subdistricts
from backend.data.demo_data import CANDIDATE_SITES, HABITATIONS, RESOURCE_INVENTORY
from backend.data.realtime_data import fetch_district_rainfall, normalize_district_name
from backend.engines.capacity_engine import calculate_capacity
from backend.engines.hazard_engine import calculate_hazard_score
from backend.engines.priority_engine import prioritize_habitation
from backend.engines.risk_engine import compute_risk
from backend.engines.resource_engine import compute_resource_readiness, estimate_resource_requirements
from backend.engines.simulation_engine import run_scenario
from backend.engines.site_engine import find_nearby_safe_sites
from backend.engines.vulnerability_engine import calculate_vulnerability_score


st.set_page_config(page_title="GARUDA Relocation Intelligence Platform", layout="wide")


@st.cache_data(ttl=1800, show_spinner=False)
def load_live_rainfall():
    return fetch_district_rainfall()


@st.cache_data
def load_census_population():
    return load_census_subdistricts()


def find_district_rainfall(district: str, rainfall_by_district: dict) -> dict | None:
    aliases = {"tehri": "tehri garhwal", "ugarkashi": "uttarkashi"}
    key = normalize_district_name(aliases.get(district.casefold(), district))
    return rainfall_by_district.get(key)

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: #090909;
        color: #f7f7f7;
        background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 32px 32px;
    }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    div[data-testid="stMetricValue"] { color: #ffffff; font-weight: 700; }
    div[data-testid="stDataFrame"] { background: rgba(255,255,255,0.03); }
    [data-testid="stSidebar"] [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]) > div { display: flex; justify-content: center; width: 100% !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.08); color: white; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def build_habitation_summary():
    rows = []
    for h in HABITATIONS:
        hazard = calculate_hazard_score(h)
        vulnerability = calculate_vulnerability_score(h)
        risk = compute_risk(h, hazard, vulnerability)
        priority = prioritize_habitation(h, risk)
        rows.append({
            "id": h["id"],
            "name": h["name"],
            "district": h["district"],
            "block": h["block"],
            "population": h["population"],
            "lat": h["lat"],
            "lon": h["lon"],
            "flood_exposure": round(h["flood_exposure"], 3),
            "landslide_exposure": round(h["landslide_exposure"], 3),
            "hazard_score": round(hazard["score_100"], 1),
            "vulnerability_score": round(vulnerability["score_100"], 1),
            "risk_score": risk["risk_score"],
            "risk_class": risk["risk_class"],
            "priority": priority["priority"],
            "history": h["disaster_history"],
            "evacuation": h["evacuation_difficulty"],
            "confidence": risk["confidence"],
        })
    return pd.DataFrame(rows)


with st.sidebar:
    st.image("GARUDA.png", width=180)
    st.caption("Prototype pilot — methodology can be extended to additional regions and hazards.")
    st.markdown("### Select Region")
    states = ["Uttarakhand"]
    selected_state = st.selectbox("State", states)
    districts = sorted(dict.fromkeys(h["district"] for h in HABITATIONS))
    selected_district = st.selectbox("District", districts)
    blocks = sorted({h["block"] for h in HABITATIONS if h["district"] == selected_district})
    selected_block = st.selectbox("Block", blocks)
    habitations = [h for h in HABITATIONS if h["district"] == selected_district and h["block"] == selected_block]
    selected_habitation = st.selectbox("Habitation/Village", [h["name"] for h in habitations])
    relocation_percent = st.slider("Scenario: % to relocate", 10, 100, 60)
    max_distance = st.slider("Maximum relocation distance (km)", 10, 50, 35)
    st.markdown("### Verification")
    status = st.selectbox("Recommendation status", ["SYSTEM GENERATED", "UNDER REVIEW", "FIELD VERIFIED", "APPROVED", "REJECTED"])

st.markdown("### GARUDA")

try:
    live_rainfall = load_live_rainfall()
    rainfall_by_district = {
        normalize_district_name(row["district"]): row for row in live_rainfall
    }
    rainfall_error = None
except Exception as error:
    rainfall_by_district = {}
    rainfall_error = str(error)

try:
    census_subdistricts = load_census_population()
    census_error = None
except Exception as error:
    census_subdistricts = {}
    census_error = str(error)
census_match_count = sum(
    find_census_subdistrict(h["district"], h["block"], census_subdistricts) is not None
    for h in HABITATIONS
)

hab_df = build_habitation_summary()
rainfall_rows = [
    find_district_rainfall(row["district"], rainfall_by_district)
    for row in HABITATIONS
]
hab_df["IMD rainfall (mm)"] = [
    observation["actual_mm"] if observation else None for observation in rainfall_rows
]
hab_df["IMD report date"] = [
    observation["report_date"] if observation else None for observation in rainfall_rows
]
selected = next(h for h in HABITATIONS if h["name"] == selected_habitation)
nearby_safe_sites = find_nearby_safe_sites(selected, CANDIDATE_SITES, max_distance)
selected_census = find_census_subdistrict(
    selected["district"], selected["block"], census_subdistricts
)
planning_population = (
    selected_census["population"] if selected_census else selected["population"]
)
planning_population_source = (
    f"2011 Census subdistrict total: {selected_census['subdistrict']}"
    if selected_census
    else "Prototype village estimate; no matching Census subdistrict"
)
selected_rainfall = find_district_rainfall(selected["district"], rainfall_by_district)
selected_hazard = calculate_hazard_score(selected)
selected_vuln = calculate_vulnerability_score(selected)
selected_risk = compute_risk(selected, selected_hazard, selected_vuln)
selected_priority = prioritize_habitation(selected, selected_risk)
resource_readiness = compute_resource_readiness(RESOURCE_INVENTORY)
scenario = run_scenario(planning_population, relocation_percent, nearby_safe_sites, RESOURCE_INVENTORY)

metrics = st.columns(4)
with metrics[0]:
    st.metric("High-risk habitations", len(hab_df[hab_df["risk_class"].isin(["High", "Very High", "Critical"])]))
with metrics[1]:
    st.metric("IMMEDIATE priority", len(hab_df[hab_df["priority"] == "IMMEDIATE"]))
with metrics[2]:
    st.metric("Nearby safe sites", len(nearby_safe_sites))
with metrics[3]:
    st.metric("Resource readiness", f"{resource_readiness['resource_readiness_percent']}%")

st.caption("Prototype pilot — methodology can be extended to additional regions and hazards.")
if rainfall_error:
    st.warning(f"Live IMD district rainfall is unavailable: {rainfall_error}")
else:
    st.info(
        "Live IMD daily district rainfall is shown as an observation overlay. "
        "Village risk baselines and relocation site capacities remain prototype values."
    )
if census_error:
    st.warning(f"2011 Census population workbook is unavailable: {census_error}")
else:
    st.info(
        f"2011 Census subdistrict totals match {census_match_count} of {len(HABITATIONS)} pilot blocks. "
        "They size relocation scenarios; village risk populations and site capacities remain prototype data."
    )

map_data = pd.DataFrame([
    {"name": h["name"], "lat": h["lat"], "lon": h["lon"], "risk": h["population"] * h["flood_exposure"]} for h in HABITATIONS
])

m = folium.Map(
    location=[selected["lat"], selected["lon"]],
    zoom_start=9,
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr='&copy; OpenStreetMap contributors',
    control_scale=True,
)
for _, row in map_data.iterrows():
    color = "red" if row["risk"] > 1500 else "orange" if row["risk"] > 1000 else "green"
    folium.CircleMarker(
        [row["lat"], row["lon"]],
        radius=8,
        color=color,
        fill=True,
        fill_opacity=0.9,
        popup=row["name"],
        tooltip=row["name"],
    ).add_to(m)

for site in nearby_safe_sites:
    folium.CircleMarker(
        [site["lat"], site["lon"]],
        radius=10,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=f"{site['name']} | {site['status']} | cap {site['land_capacity']}",
        tooltip=site["name"],
    ).add_to(m)

st_folium(m, width=1400, height=420)

risk_tabs = st.tabs(["Overview", "Risk & Priority", "Sites & Capacity", "Resources", "Simulation", "AI Assistant"])

with risk_tabs[0]:
    sel_cols = st.columns([2, 1, 1, 1, 1])
    with sel_cols[0]:
        st.markdown(f"### {selected['name']}")
        st.write(f"District: {selected['district']}")
        st.write(f"Block: {selected['block']}")
        st.write(f"Prototype village population (risk baseline): {selected['population']:,}")
        if selected_census:
            st.metric("2011 Census planning population", f"{planning_population:,}")
            st.caption(f"Total for the {selected_census['subdistrict']} subdistrict, not village-only.")
        else:
            st.caption("No matching 2011 Census subdistrict; planning uses the prototype village estimate.")
        st.write(f"Disaster history: {selected['disaster_history']}")
        if selected_rainfall:
            st.metric("IMD rainfall (daily)", f"{selected_rainfall['actual_mm']:.1f} mm")
            st.caption(f"Report date: {selected_rainfall['report_date']}")
        else:
            st.caption("No matching live IMD district rainfall observation.")
    with sel_cols[1]:
        st.metric("Hazard", f"{selected_hazard['score_100']:.1f}/100")
    with sel_cols[2]:
        st.metric("Vulnerability", f"{selected_vuln['score_100']:.1f}/100")
    with sel_cols[3]:
        st.metric("Risk class", selected_risk["risk_class"])
    with sel_cols[4]:
        st.metric("Priority", selected_priority["priority"])

    st.markdown(f"**Why this habitation is prioritized:** {selected_priority['explanation']}")
    st.write(f"**Major factors:** {', '.join(selected_risk['major_factors'])}")

    st.subheader("Live IMD district rainfall")
    rainfall_table = []
    for district in dict.fromkeys(habitation["district"] for habitation in HABITATIONS):
        observation = find_district_rainfall(district, rainfall_by_district)
        rainfall_table.append({
            "District": district,
            "Report date": observation["report_date"] if observation else "Unavailable",
            "Actual rainfall (mm)": observation["actual_mm"] if observation else None,
            "Normal rainfall (mm)": observation["normal_mm"] if observation else None,
            "Departure (%)": observation["departure_percent"] if observation else None,
        })
    st.dataframe(pd.DataFrame(rainfall_table), hide_index=True, use_container_width=True)

with risk_tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Hazard Assessment")
        hazard_df = pd.DataFrame([{"Factor": factor, "Contribution": value} for factor, value in selected_hazard["components"].items()])
        st.dataframe(hazard_df, hide_index=True)
    with c2:
        st.subheader("Vulnerability Assessment")
        vuln_df = pd.DataFrame([{"Factor": factor, "Contribution": value} for factor, value in selected_vuln["components"].items()])
        st.dataframe(vuln_df, hide_index=True)

    st.subheader("Risk Engine")
    r1, r2, r3, r4 = st.columns([1, 1, 1, 1.2])
    with r1: st.metric("Risk score", f"{selected_risk['risk_score']:.1f}/100")
    with r2: st.metric("Risk class", selected_risk["risk_class"])
    with r3: st.metric("Confidence", f"{selected_risk['confidence'] * 100:.0f}%")
    with r4:
        st.metric(
            "IMD rain report",
            selected_rainfall["report_date"] if selected_rainfall else "Unavailable",
        )
    st.markdown("> AI-assessed high-risk zone — Candidate Red Zone — requires authority verification")

with risk_tabs[2]:
    st.subheader("Safe-site discovery")
    st.caption(
        f"Showing safe sites within {max_distance} km of {selected['name']} "
        f"({selected['lat']:.3f}, {selected['lon']:.3f})."
    )
    capacity_metrics = st.columns(4)
    with capacity_metrics[0]:
        st.metric("2011 planning population", f"{planning_population:,}")
    with capacity_metrics[1]:
        st.metric("Planned relocation", f"{scenario['relocated']:,}")
    with capacity_metrics[2]:
        st.metric("Effective safe-site capacity", f"{scenario['capacity_available']:,}")
    with capacity_metrics[3]:
        st.metric("Capacity gap", f"{scenario['capacity_gap']:,}")
    st.caption(
        f"Population basis: {planning_population_source}. "
        "Site capacity figures are prototype constraints; effective capacity uses the lowest constraint per site."
    )

    safe_sites = []
    for site in nearby_safe_sites:
        capacity = calculate_capacity(site)
        safe_sites.append({
            "Site": site["name"],
            "Distance (km)": round(site["distance_km"], 1),
            "Status": site["status"],
            "Effective Capacity": capacity["effective_capacity"],
            "Limiting Factor": capacity["limiting_factor"],
            "Suitability": site["suitability_score"],
        })
    st.dataframe(pd.DataFrame(safe_sites), use_container_width=True)

    st.subheader("Prototype site capacity breakdown")
    for site in nearby_safe_sites:
        capacity = calculate_capacity(site)
        with st.container():
            st.markdown(f"#### {site['name']} · {site['distance_km']:.1f} km")
            cap_cols = st.columns(6)
            capacities = [site["land_capacity"], site["water_capacity"], site["road_capacity"], site["healthcare_capacity"], site["school_capacity"], site["environmental_capacity"]]
            labels = ["Land", "Water", "Road", "Healthcare", "School", "Environment"]
            for idx, label in enumerate(labels):
                with cap_cols[idx]:
                    st.metric(label, capacities[idx])
            st.caption(f"Effective capacity: {capacity['effective_capacity']} | Limiting factor: {capacity['limiting_factor']}")

with risk_tabs[3]:
    st.subheader("Resource management dashboard")
    res_df = pd.DataFrame(RESOURCE_INVENTORY)[["name", "location", "total_quantity", "available_quantity", "deployed_quantity", "status"]]
    st.dataframe(res_df, use_container_width=True)
    st.write("Prototype planning assumptions")
    req = estimate_resource_requirements(scenario["relocated"])
    st.json(req)
    st.caption(f"Requirements use {scenario['relocated']:,} planned relocations from {planning_population_source}.")
    st.metric("Emergency readiness", f"{resource_readiness['resource_readiness_percent']}%")
    st.caption(f"Critical shortages: {resource_readiness['critical_shortages']}")

with risk_tabs[4]:
    st.subheader("What-if relocation simulator")
    baseline = run_scenario(planning_population, 100, nearby_safe_sites, RESOURCE_INVENTORY)
    scenario_text = (
        f"BASELINE\nPlanning population: {planning_population}\nRelocation capacity: {baseline['capacity_available']}\n"
        f"Capacity gap: {baseline['capacity_gap']}\n\nSCENARIO\nPopulation relocated: {scenario['relocated']}\n"
        f"Capacity available: {scenario['capacity_available']}\nCapacity gap: {scenario['capacity_gap']}"
    )
    st.text(scenario_text)
    st.write("Site capacities and resource inventory are prototype values.")
    st.json({
        "planning_population": planning_population,
        "population_basis": planning_population_source,
        "population_to_relocate": scenario["relocated"],
        "capacity_gap": scenario["capacity_gap"],
        "resource_gap": scenario["resource_gap"],
    })

with risk_tabs[5]:
    st.subheader("AI Assistant")
    q = st.text_input("Ask GARUDA", "Why is this village prioritized?")
    if q:
        ans = answer_question(q, HABITATIONS, CANDIDATE_SITES, RESOURCE_INVENTORY)
        st.json(ans)

st.subheader("Officer verification workflow")
st.write(f"Current recommendation status: {status}")
st.caption("System-generated recommendation is advisory only; authority approval remains human-led and field verification may require local validation.")

st.caption("Risk calculations are deterministic, explainable, and constrained to the supported pilot dataset. We do not claim legal red-zone designation.")
