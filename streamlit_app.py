from __future__ import annotations

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

from backend.ai_assistant import answer_question
from backend.data.demo_data import CANDIDATE_SITES, HABITATIONS, RESOURCE_INVENTORY
from backend.engines.capacity_engine import calculate_capacity
from backend.engines.hazard_engine import calculate_hazard_score
from backend.engines.priority_engine import prioritize_habitation
from backend.engines.risk_engine import compute_risk
from backend.engines.resource_engine import compute_resource_readiness, estimate_resource_requirements
from backend.engines.simulation_engine import run_scenario
from backend.engines.site_engine import evaluate_site
from backend.engines.vulnerability_engine import calculate_vulnerability_score


st.set_page_config(page_title="GARUDA Relocation Intelligence Platform", layout="wide")

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


@st.cache_data
def build_site_summary():
    summary = []
    for site in CANDIDATE_SITES:
        capacity = calculate_capacity(site)
        summary.append({
            "id": site["id"],
            "name": site["name"],
            "district": site["district"],
            "status": site["status"],
            "distance_km": site["distance_km"],
            "effective_capacity": capacity["effective_capacity"],
            "limiting_factor": capacity["limiting_factor"],
            "suitability_score": evaluate_site(site, HABITATIONS[0])["suitability_score"],
        })
    return pd.DataFrame(summary)


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

hab_df = build_habitation_summary()
site_df = build_site_summary()
selected = next(h for h in HABITATIONS if h["name"] == selected_habitation)
selected_hazard = calculate_hazard_score(selected)
selected_vuln = calculate_vulnerability_score(selected)
selected_risk = compute_risk(selected, selected_hazard, selected_vuln)
selected_priority = prioritize_habitation(selected, selected_risk)
resource_readiness = compute_resource_readiness(RESOURCE_INVENTORY)
scenario = run_scenario(selected["population"], relocation_percent, CANDIDATE_SITES, RESOURCE_INVENTORY)

metrics = st.columns(4)
with metrics[0]:
    st.metric("High-risk habitations", len(hab_df[hab_df["risk_class"].isin(["High", "Very High", "Critical"])]))
with metrics[1]:
    st.metric("IMMEDIATE priority", len(hab_df[hab_df["priority"] == "IMMEDIATE"]))
with metrics[2]:
    st.metric("Safe sites", len(site_df[site_df["status"] == "SAFE"]))
with metrics[3]:
    st.metric("Resource readiness", f"{resource_readiness['resource_readiness_percent']}%")

st.caption("Prototype pilot — methodology can be extended to additional regions and hazards.")

map_data = pd.DataFrame([
    {"name": h["name"], "lat": h["lat"], "lon": h["lon"], "risk": h["population"] * h["flood_exposure"]} for h in HABITATIONS
])

m = folium.Map(
    location=[30.4, 79.0],
    zoom_start=7,
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

for site in CANDIDATE_SITES:
    color = "green" if site["status"] == "SAFE" else "red"
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
        st.write(f"Population: {selected['population']}")
        st.write(f"Disaster history: {selected['disaster_history']}")
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
    with r4: st.metric("Data freshness", "2025-2026")
    st.markdown("> AI-assessed high-risk zone — Candidate Red Zone — requires authority verification")

with risk_tabs[2]:
    st.subheader("Safe-site discovery")
    safe_sites = []
    for site in CANDIDATE_SITES:
        evaluation = evaluate_site(site, selected)
        capacity = calculate_capacity(site)
        if evaluation["status"] == "SAFE":
            safe_sites.append({
                "Site": site["name"],
                "Distance (km)": site["distance_km"],
                "Status": evaluation["status"],
                "Effective Capacity": capacity["effective_capacity"],
                "Limiting Factor": capacity["limiting_factor"],
                "Suitability": evaluation["suitability_score"],
            })
    st.dataframe(pd.DataFrame(safe_sites), use_container_width=True)

    st.subheader("Site capacity breakdown")
    for site in CANDIDATE_SITES:
        capacity = calculate_capacity(site)
        if site["status"] == "SAFE":
            with st.container():
                st.markdown(f"#### {site['name']}")
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
    req = estimate_resource_requirements(selected["population"])
    st.json(req)
    st.metric("Emergency readiness", f"{resource_readiness['resource_readiness_percent']}%")
    st.caption(f"Critical shortages: {resource_readiness['critical_shortages']}")

with risk_tabs[4]:
    st.subheader("What-if relocation simulator")
    baseline = run_scenario(selected["population"], 100, CANDIDATE_SITES, RESOURCE_INVENTORY)
    scenario_text = (
        f"BASELINE\nPopulation exposed: {selected['population']}\nRelocation capacity: {baseline['capacity_available']}\n"
        f"Capacity gap: {baseline['capacity_gap']}\n\nSCENARIO\nPopulation relocated: {scenario['relocated']}\n"
        f"Capacity available: {scenario['capacity_available']}\nCapacity gap: {scenario['capacity_gap']}"
    )
    st.text(scenario_text)
    st.write("Prototype configured scenario values")
    st.json({"population_to_relocate": scenario['relocated'], "capacity_gap": scenario['capacity_gap'], "resource_gap": scenario['resource_gap']})

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
