You are a senior GIS + AI systems engineer building an MVP for a Smart India Hackathon 2026 problem on **AI-driven proactive disaster relocation planning in India**.

name- Garuda- AI-Driven Risk Assessment & Relocation Intelligence Platform

## We'll deploy the system using streamlit, so keep that noted while building. 
## the theme of overall system will be black & white. use main background as black with white translucent grid
## create necessary changes to add resource system too.
## use main logo from garuda.png and icons from other .png files

## 1. Problem
Develop an **AI-driven GIS Decision Support Platform for Proactive Disaster Relocation**.
The system must help disaster-management authorities answer four practical questions:
1. Which habitations are currently exposed to significant multi-hazard risk?
2. Which vulnerable habitations should be prioritized for relocation?
3. Where can the affected population potentially relocate safely?
4. Can the proposed relocation site actually accommodate them, and what infrastructure gaps exist?
The MVP must demonstrate the complete chain:
**Data → Validation → GIS Risk Assessment → Relocation Priority → Safe-Site Discovery → Capacity Assessment → Site Matching → Explainable Recommendation**
Do NOT build a generic disaster dashboard.
Do NOT make the LLM responsible for numerical risk calculations or final decisions.
The system's numerical decisions must come from deterministic GIS/ML/optimization logic. AI should be used for interpretation, natural-language querying, explanation, and report generation.
---
# 2. MVP Scope
Do NOT attempt to cover all of India.
Use one representative pilot region, preferably:
**Uttarakhand**
Focus initially on two hazards:
* Flood
* Landslide
The architecture must remain extensible to additional hazards such as:
* Cloudburst
* Earthquake
* Coastal erosion
* Cyclone
The UI should clearly state:
> "Prototype pilot — methodology can be extended to additional regions and hazards."
---
# 3. Core MVP Workflow
Implement this exact workflow:
### STEP 1 — Select Region
User selects:
* State
* District
* Block
* Habitation/Village
Display the selected habitation on the map.
Show:
* Population
* Hazard exposure
* Vulnerability
* Disaster history
* Accessibility
* Current infrastructure context
---
### STEP 2 — Hazard Assessment
Create a GIS-based hazard assessment engine.
For each habitation calculate normalized values between 0 and 1:
```
Flood Exposure
Landslide Exposure
Historical Disaster Impact
Accessibility Risk
```
Example:
```
Hazard Score =
    0.40 × Flood Exposure
  + 0.35 × Landslide Exposure
  + 0.25 × Historical Disaster Impact
```
Make weights configurable.
Do NOT claim that these weights are scientifically universal.
Label them as:
> "Prototype configurable weights."
The system must display the individual contributions rather than only showing the final score.
---
# 4. Vulnerability Engine
Calculate a vulnerability score using available demographic and infrastructure information.
Possible factors:
```
Population vulnerability
+
Housing vulnerability
+
Healthcare accessibility
+
Road accessibility
+
Evacuation accessibility
+
Critical infrastructure availability
```
Example:
```
Vulnerability Score =
    0.30 × Population Vulnerability
  + 0.20 × Housing Vulnerability
  + 0.20 × Healthcare Accessibility Risk
  + 0.15 × Road Accessibility Risk
  + 0.15 × Evacuation Difficulty
```
All values must be normalized.
Show the individual components in the UI.
---
# 5. Risk Engine
Calculate:
```
Risk =
Hazard Exposure × Vulnerability
```
Convert to a 0–100 score.
Example classification:
```text
0–20       Low
20–40      Moderate
40–60      High
60–80      Very High
80–100     Critical
```
These thresholds must be configurable.
Display:
* Risk score
* Risk class
* Confidence
* Major contributing factors
* Data freshness
* Data sources
IMPORTANT:
Do not claim that the system legally declares a "Red Zone".
Instead use:
> "AI-assessed high-risk zone"
and:
> "Candidate Red Zone — requires authority verification"
---
# 6. Relocation Priority Engine
Calculate a relocation priority score based on:
```text
Risk
+
Population Vulnerability
+
Historical Disaster Impact
+
Exposed Population
+
Evacuation Difficulty
```
Output:
```text
IMMEDIATE
SHORT-TERM
MEDIUM-TERM
MONITOR
```
For every priority recommendation provide an explanation.
Example:
```
Relocation Priority: IMMEDIATE
Why?
• Very high landslide exposure
• High flood exposure
• 1,842 residents exposed
• Limited evacuation connectivity
• Repeated disaster incidents
• High elderly/child population
```
Do not merely display a score.
---
# 7. Safe Relocation Site Discovery
This is one of the most important differentiating components of the MVP.
When a habitation is selected, generate possible relocation sites.
Candidate sites can initially come from:
* low-risk land polygons
* government/public land in prototype data
* open areas
* existing settlement expansion zones
* manually defined candidate polygons for the demo
Each candidate site must be evaluated against:
### HARD CONSTRAINTS
Reject a site if:
```
Inside high-risk flood zone
OR
Inside high-risk landslide zone
OR
Environmentally restricted
OR
No reasonable road access
OR
Insufficient usable land
```
### SOFT CONSTRAINTS
Score the remaining sites using:
```
Distance from original habitation
Road accessibility
Healthcare accessibility
School accessibility
Water availability
Existing infrastructure
Environmental suitability
Residual hazard
Development requirement
```
---
# 8. Effective Carrying Capacity
Do NOT simply calculate:
```
land area / area per person
```
Instead calculate capacity across multiple infrastructure dimensions.
For each candidate site calculate:
```text
Land Capacity
Water Capacity
Road Capacity
Healthcare Capacity
School Capacity
Environmental Capacity
```
Then:
```
Effective Carrying Capacity =
MIN(
    Land Capacity,
    Water Capacity,
    Road Capacity,
    Healthcare Capacity,
    School Capacity,
    Environmental Capacity
)
```
Display the limiting factor.
Example:
```
Candidate Site A
Effective Capacity: 1,200 people

Land capacity:        2,100
Water capacity:       1,500
Road capacity:        1,700
Healthcare capacity:  1,200
School capacity:      1,450
Environmental limit:  1,800

LIMITING FACTOR:
Healthcare capacity
```
This should be a visually prominent part of the dashboard.
---
# 9. Relocation Matching Engine
Match vulnerable habitations to candidate relocation sites.
Example:
```
Village population = 1,800

Site A capacity = 1,000
Site B capacity = 1,200
```
The system should be able to recommend:
```
Site A → 1,000 people
Site B → 800 people
```
Subject to:
* site capacity
* safety
* maximum acceptable distance
* infrastructure constraints
* residual risk
The optimization objective should minimize:
```
Relocation Distance
+
Infrastructure Deficit
+
Residual Risk
+
Development Cost
```
while satisfying:
```
Population Allocation <= Site Capacity
```
Use **Google OR-Tools** or an equivalent optimization library.
---
# 10. What-If Relocation Simulator
Implement a simple scenario simulator.
Allow the authority to change:
```
Population to relocate
Percentage relocated
Candidate sites
Maximum relocation distance
Infrastructure investment
Risk threshold
```
Example:
```
Current population:
2,500
Scenario:
Relocate 60%
Population relocated:
1,500
```
The system recalculates:
* site allocation
* remaining capacity
* infrastructure deficit
* total distance
* estimated relocation requirement
Provide a clear comparison:
```
BASELINE
Population exposed: 2,500
Relocation capacity: 1,200
Capacity gap: 1,300

SCENARIO
Population relocated: 1,500
Capacity available: 1,700
Capacity gap: 0
Healthcare gap: ₹X
Water gap: ₹Y
```
This simulator is important because it demonstrates that the platform is a **decision-support system**, not merely a mapping application.
---
# 11. Explainability Layer
Every major system output must have an explanation.
For example:
```json
{
  "decision": "IMMEDIATE_RELOCATION",
  "score": 87,
  "confidence": 0.82,
  "drivers": [
    {
      "factor": "Landslide exposure",
      "contribution": 31
    },
    {
      "factor": "Population vulnerability",
      "contribution": 22
    },
    {
      "factor": "Historical disaster impact",
      "contribution": 18
    }
  ],
  "data_sources": [
    "Hazard dataset",
    "Population dataset",
    "Road network"
  ],
  "data_freshness": {
    "population": "2011 baseline",
    "hazard": "2025",
    "roads": "2026"
  }
}
```
The frontend should convert this into a human-readable explanation.
---
# 12. AI Assistant
Add an AI assistant, but constrain its role.
The AI assistant must NOT independently calculate risk.
Architecture:
```
User Question
      ↓
AI Query Interpreter
      ↓
Structured GIS Query
      ↓
GIS/Risk/Site APIs
      ↓
Verified Numerical Results
      ↓
AI Explanation
```
Support queries such as:

> "Show villages with very high risk and population above 2,000."

> "Why is this village prioritized for immediate relocation?"

> "Which relocation site can accommodate the largest population?"

> "What is limiting Site B's capacity?"

> "What happens if we relocate 70% of the population?"

The AI should answer using system-generated results rather than inventing values.
---
# 13. Data Sources
Structure the system so external datasets can eventually be connected.
Prototype data should represent data obtainable from sources such as:
### Disaster / Hazard
* ISRO / NRSC
* Bhuvan
* NDEM
* Landslide inventories
* Flood hazard datasets
### Population
* Census of India
### Weather
* India Meteorological Department
### Roads / Infrastructure
* OpenStreetMap
### Elevation
* SRTM / DEM
### Satellite
* Copernicus Sentinel
### Field Data
Create a prototype field-verification interface allowing an officer to submit:
* GPS location
* photo
* road condition
* water availability
* infrastructure status
* local observations
IMPORTANT:
Do not pretend unavailable APIs or restricted datasets are freely accessible.
Create an abstraction layer:
```text
DataSource
   ↓
DataAdapter
   ↓
Normalized Internal Schema
```
This allows real datasets to be plugged in later.
---
# 14. Database
Use:
**PostgreSQL + PostGIS**
Core entities:
```
users
administrative_units
habitations
population_profiles
hazard_layers
hazard_observations
disaster_events
infrastructure
roads
candidate_sites
site_assessments
site_capacity
risk_assessments
priority_assessments
relocation_plans
relocation_allocations
simulation_runs
field_reports
data_sources
dataset_versions
audit_logs
```
Use PostGIS geometry types.
Examples:
```
POINT
LINESTRING
POLYGON
MULTIPOLYGON
```
Create spatial indexes.
Use proper foreign-key relationships.
---
# 15. Data Validation
Before any dataset enters the analytical pipeline, validate:
### Schema
* required fields
* data types
* null values
### Geospatial
* valid geometry
* correct CRS
* geometry overlaps
* coordinates inside expected region
### Temporal
* dataset date
* observation date
* freshness
### Consistency
Examples:
```text
population >= 0
capacity >= 0
area > 0
latitude/longitude valid
```
Generate a:
```
Data Quality Score
```
Do not allow low-quality data to silently influence critical recommendations.
---
# 16. Data Confidence
Every analytical result must contain:
```
Score
Confidence
Data freshness
Source
```
Example:
```
Risk Score: 82/100
Confidence: 78%
Confidence reduced because:
• population data is based on 2011 Census
• latest local infrastructure data unavailable
```
This is important for government decision support.
---
## RESOURCE & EMERGENCY CAPACITY MANAGEMENT
Add a dedicated Resource Management module to the disaster-relocation platform.
The purpose is to maintain an authority-controlled inventory of resources and determine whether available resources are sufficient to support emergency response and relocation plans.
The module must NOT be an independent inventory system.
It must directly interact with:
* Risk Engine
* Relocation Priority Engine
* Candidate Site Engine
* Carrying Capacity Engine
* Relocation Optimizer
* What-if Simulator
---
### 1. Resource Categories
Support the following categories.
#### Emergency Response Resources
* Ambulances
* Rescue vehicles
* Boats
* Earthmovers
* Emergency shelters
* Medical kits
* Food supplies
* Water supplies
* Tents
* Blankets
* Rescue equipment
* Communication equipment
* Emergency personnel
* Medical personnel
#### Relocation Resources
* Temporary shelters
* Available housing
* Transport vehicles
* Water tankers
* Food storage
* Medical facilities
* Sanitation facilities
* Electricity availability
* School capacity
* Healthcare capacity
#### Infrastructure Capacity
* Water capacity
* Healthcare capacity
* School capacity
* Road/transport capacity
* Shelter capacity
* Electricity capacity
* Sanitation capacity
---
### 2. Authority Resource Management
Provide an authority dashboard where authorized users can:
* Add resources
* Update resource quantities
* Mark resources as deployed
* Mark resources as unavailable
* Update resource location
* Update capacity
* Record last-updated timestamp
* Add notes
* View resource history
Example:
```
Resource:
Water Tanker
Location:
District A
Total:
20
Available:
13
Deployed:
7
Status:
AVAILABLE
Last Updated:
30 Sep 2026
```
Changes must immediately affect the analytical system where applicable.
---
### 3. Resource Database Model
Create:
```
resources
resource_types
resource_locations
resource_allocations
resource_movements
resource_updates
```
Example schema:
```
resources
---------
id
resource_type_id
location_id
total_quantity
available_quantity
deployed_quantity
unit
capacity
status
last_updated
updated_by
notes
```
Maintain an audit trail for every authority update.
---
### 4. Resource Allocation
When a relocation plan is generated, calculate required resources.
Example:
```
Population to relocate:
2,000
```
Calculate requirements such as:
```
Water requirement
Medical requirement
Shelter requirement
Transport requirement
Food requirement
```
Use configurable planning coefficients rather than hard-coding universal values.
For example:
```
water_required =
population × configurable_water_requirement
```
Clearly label these as:
> "Prototype planning assumptions"
unless supported by an authoritative standard.
---
### 5. Resource Sufficiency
For every relocation plan calculate:
```
Required
Available
Deficit
Surplus
```
Example:
```
RESOURCE SUFFICIENCY
                    Required    Available    Status
----------------------------------------------------
Shelter               2,000       2,200      ✓
Water                  4,000       3,200      ⚠
Medical kits           2,000       2,600      ✓
Transport vehicles        40          28      ⚠
Food packages          6,000       7,500      ✓
```
Show deficits prominently.
---
### 6. Resource-Aware Site Capacity
Resource availability must influence effective carrying capacity.
For each candidate relocation site calculate:
```
Land Capacity
Water Capacity
Healthcare Capacity
Shelter Capacity
School Capacity
Road Capacity
Environmental Capacity
```
Then:
```
Effective Capacity =
MIN(
    Land Capacity,
    Water Capacity,
    Healthcare Capacity,
    Shelter Capacity,
    School Capacity,
    Road Capacity,
    Environmental Capacity
)
```
Display the limiting factor.
Example:
```
SITE B
Land:          2,400
Water:         1,500
Healthcare:    2,000
Shelter:       1,800
Road:          2,100
Effective Capacity:
1,500 people
Limiting factor:
WATER
```
---
### 7. Resource-Aware Relocation Optimization
The relocation optimizer must consider both:
#### Population constraints
```
allocated_population <= effective_site_capacity
```
and:
#### Resource constraints
```
required_resource <= available_resource
```
The optimizer should minimize a configurable objective containing:
```
Relocation distance
+
Infrastructure deficit
+
Resource deficit
+
Residual hazard
+
Estimated development cost
```
Do not allow an unsafe site to become acceptable simply because it has more resources.
Safety-related hard constraints must always be evaluated first.
---
### 8. Resource Deployment
Allow authorities to allocate resources to:
* Habitations
* Shelters
* Candidate relocation sites
* Emergency response zones
Example:
```
Village A
Risk: CRITICAL
Requested:
5 ambulances
2 rescue vehicles
1 medical team
3 water tankers
Available:
3 ambulances
1 rescue vehicle
2 water tankers
Deficit:
2 ambulances
1 rescue vehicle
```
---
### 9. Resource Map Layer
Display resources geographically.
Map layers:
```
Emergency Shelters
Hospitals
Ambulances
Rescue Teams
Water Sources
Food Stores
Rescue Equipment
Candidate Relocation Sites
```
Clicking a resource should show:
```
Resource
Location
Quantity
Availability
Capacity
Current deployment
Last update
```
---
### 10. Resource Status
Use:
```
AVAILABLE
PARTIALLY_DEPLOYED
DEPLOYED
UNAVAILABLE
UNDER_MAINTENANCE
```
Do not use visual status alone.
Always provide the underlying numerical quantity.
---
### 11. Resource Update History
Every modification must create an audit record:
```
resource_id
previous_quantity
new_quantity
previous_status
new_status
updated_by
timestamp
reason
```
Example:
```
Water Tanker #17
Previous:
Available = 5
Updated:
Available = 3
Reason:
2 tankers deployed to Village A
Updated by:
District Authority
Time:
10:42 AM
```
---
### 12. What-If Resource Simulation
Integrate resource management into the existing simulation engine.
Allow an authority to simulate:
```
What if 70% of Village A is relocated?
What if two water tankers become unavailable?
What if a temporary shelter with 500 capacity is added?
What if healthcare capacity is increased by 20%?
What if 3 ambulances are deployed to another district?
```
Recalculate:
* effective capacity
* resource deficits
* relocation allocation
* infrastructure gaps
* site suitability
* overall relocation feasibility
---
### 13. Resource Intelligence Dashboard
Add a dashboard section:
```
RESOURCE READINESS
Emergency resources available: 78%
Shelter capacity: 86%
Water availability: 61%
Medical readiness: 92%
Transport availability: 73%
Critical shortages: 4
```
The dashboard must allow the authority to drill down into the numbers.
---
### 14. AI Integration
The AI assistant may answer questions such as:
> "How many ambulances are currently available in this district?"
> "Which relocation sites have insufficient water capacity?"
> "What resources are required to relocate 2,000 people?"
> "Which resource shortages are currently limiting relocation?"
> "What happens if three water tankers are deployed to Village A?"
The AI must retrieve these values from the database and analytical engines.
It must NOT invent resource quantities.
Architecture:
```
User
 ↓
AI Query Interpreter
 ↓
Resource / GIS / Analytics Tools
 ↓
Verified Data
 ↓
AI Explanation
```
---
### 15. Resource Management Success Criterion
The evaluator should be able to perform this demonstration:
```
Select high-risk habitation
        ↓
System calculates relocation priority
        ↓
Find safe relocation sites
        ↓
Calculate site capacities
        ↓
Check available resources
        ↓
Identify resource deficits
        ↓
Authority adds/updates resource
        ↓
System recalculates capacity
        ↓
Relocation plan becomes feasible
        ↓
Generate explainable plan
```
The module must demonstrate that resource availability is not merely displayed.
It must **affect relocation feasibility and planning decisions**.

---
# 17. GIS Dashboard
Create a professional authority-facing dashboard.
Layout:
```
---------------------------------------------------------
| Header: Disaster Relocation Intelligence Platform    |
---------------------------------------------------------
|                                                       |
|                     MAP                               |
|                                                       |
|       Hazard layers / Villages / Sites               |
|                                                       |
---------------------------------------------------------
| Risk | Vulnerability | Priority | Sites | Capacity  |
---------------------------------------------------------
| Selected Habitation Details                          |
---------------------------------------------------------
```
Map controls:
```
Flood Risk
Landslide Risk
Multi-Hazard Risk
Population
Vulnerability
Disaster History
Candidate Relocation Sites
Roads
Hospitals
Schools
Water Sources
```
Clicking a habitation should open a detailed panel.
---
# 18. Technology Stack
Use:
### Frontend
```
React
TypeScript
Tailwind CSS
MapLibre GL JS
Recharts
```
### Backend
```
Python
FastAPI
Pydantic
SQLAlchemy
JWT authentication
```
### GIS
```
GeoPandas
Shapely
Rasterio
GDAL
PyProj
PostGIS
```
### Analytics / ML
```
NumPy
Pandas
Scikit-learn
XGBoost
```
Use ML only where justified by available training/data.
Do not add ML simply to call the system "AI".
### Optimization
```
Google OR-Tools
```
### AI
Use a modern LLM API such as Gemini.
Use:
* structured outputs
* function/tool calling
* controlled prompts
Optional:
```
pgvector
```
for document/evidence retrieval.
### Deployment
```
Docker
Google Cloud Run
Cloud SQL
Cloud Storage
```
The application should also run completely locally for demonstration.
---
# 19. Backend Architecture
Use a modular monolith.
Do NOT create unnecessary microservices.
Recommended structure:
```
make necessary changes to accommodate resource management system.
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── hazards.py
│   │   ├── habitations.py
│   │   ├── risk.py
│   │   ├── relocation.py
│   │   ├── sites.py
│   │   ├── simulation.py
│   │   └── ai.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── data_validation/
│   │   ├── hazard_engine/
│   │   ├── vulnerability_engine/
│   │   ├── risk_engine/
│   │   ├── priority_engine/
│   │   ├── site_engine/
│   │   ├── capacity_engine/
│   │   ├── optimization_engine/
│   │   └── simulation_engine/
│   │
│   ├── gis/
│   │
│   └── ai/
│
├── tests/
├── seed/
├── migrations/
├── Dockerfile
└── requirements.txt
```
---
# 20. Frontend Architecture
```
make necessary changes to accommodate resource management system.
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── maps/
│   ├── charts/
│   ├── panels/
│   ├── api/
│   ├── hooks/
│   ├── types/
│   └── utils/
│
└── ...
```

Create reusable components for:
```
RiskCard
PriorityCard
HazardLayerControl
SiteCard
CapacityBreakdown
InfrastructureGap
ExplainabilityPanel
SimulationPanel
AIChat
DataFreshnessBadge
ConfidenceBadge
```
---
# 21. Demonstration Dataset
Create a realistic synthetic dataset for the selected pilot region if official datasets cannot be directly integrated during MVP development.
IMPORTANT:
Clearly label synthetic/demo data.
For example:
```
DATA STATUS
Population:
Census baseline
Hazard:
Prototype hazard layer
Infrastructure:
OpenStreetMap / prototype
Relocation Sites:
Demonstration dataset
```
Never present synthetic values as official government data.
Create at least:
```
20–50 habitations
10–20 candidate relocation sites
roads
rivers
schools
hospitals
water sources
historical disaster events
flood risk polygons
landslide risk polygons
```
The data should produce meaningful differences between villages and candidate sites.
---
# 22. Demo Scenario
The MVP must have one polished end-to-end scenario.
Example:
### Village A
```
Population: 2,400
Flood Exposure: 0.82
Landslide Exposure: 0.71
Vulnerability: 0.78
Historical Impact: 0.65
Risk Score: 83/100
Priority:
IMMEDIATE
```
The system then identifies:
```
Site A
Capacity: 1,000

Site B
Capacity: 1,800

Site C
Rejected
Reason: High landslide exposure
```
Optimization:
```
Site A → 900 people
Site B → 1,500 people
```
Then show:
```
Total population relocated: 2,400
Capacity constraint: satisfied
Remaining infrastructure gap:
Healthcare: 12%
Water: 8%
Road: 5%
```
Finally ask the AI:
> "Why was Village A prioritized?"
The AI generates an explanation from the verified system results.
---
# 23. Critical UX Requirement
The evaluator must understand the system within **60 seconds**.
The landing dashboard should immediately show:
```
HIGH-RISK HABITATIONS
      ↓
RELOCATION PRIORITY
      ↓
AVAILABLE SAFE SITES
      ↓
SITE CAPACITY
      ↓
RECOMMENDED ALLOCATION
```
Do not bury the core innovation inside menus.
---
# 24. Authority Verification Workflow
Include:
```
AI/System Assessment
        ↓
Officer Review
        ↓
Field Verification
        ↓
Authority Approval
```
A recommendation should have status:
```
SYSTEM GENERATED
UNDER REVIEW
FIELD VERIFIED
APPROVED
REJECTED
```
This makes clear that the platform is a decision-support system rather than an autonomous authority.
---
# 25. Audit Trail
For every recommendation store:
```
timestamp
user
dataset versions
risk model version
weights
input values
calculated score
recommendation
simulation parameters
approval status
```
Allow the evaluator to open:
> "Why did the system recommend this?"
and see the evidence chain.
---
# 26. Quality Requirements
The application must be:
* responsive
* visually polished
* fast enough for a live demo
* modular
* explainable
* reproducible
* locally runnable
* Dockerized
* API documented through FastAPI/OpenAPI
* backed by automated tests
Include tests for:
```
risk calculation
capacity calculation
hard site constraints
priority calculation
allocation constraints
data validation
simulation
```
---
# 27. What NOT to Build
Do NOT waste MVP development time on:
* dozens of AI agents
* generic chatbot functionality
* fake real-time disaster feeds
* nationwide coverage
* unnecessary microservices
* complex deep-learning models without training data
* decorative 3D maps
* arbitrary "AI-generated" risk scores
* claiming legal Red Zone designation
* fabricated government datasets
* unsupported predictions
* a dashboard with no actionable recommendation
The MVP must prioritize **decision usefulness over feature count**.
---
# 28. Final Success Criterion
The finished prototype must demonstrate this complete journey:
```
SELECT HABITATION
        ↓
ASSESS MULTI-HAZARD RISK
        ↓
ASSESS VULNERABILITY
        ↓
CALCULATE RELOCATION PRIORITY
        ↓
GENERATE SAFE-SITE CANDIDATES
        ↓
FILTER UNSAFE SITES
        ↓
CALCULATE EFFECTIVE CAPACITY
        ↓
MATCH POPULATION TO SITES
        ↓
IDENTIFY INFRASTRUCTURE GAPS
        ↓
RUN WHAT-IF SCENARIO
        ↓
EXPLAIN RECOMMENDATION
        ↓
OFFICER VERIFICATION
```
The final product should feel like:
> **"A relocation planning cockpit for disaster-management authorities."**
—not a disaster map, not a chatbot, and not a generic AI dashboard.
## Deliverables
Produce:
1. Complete source code
2. Database schema
3. PostGIS setup
4. Seed/demo dataset
5. Data ingestion interfaces
6. Risk calculation engine
7. Vulnerability engine
8. Relocation priority engine
9. Safe-site discovery engine
10. Effective carrying-capacity engine
11. Relocation optimization engine
12. What-if simulator
13. Explainability layer
14. AI assistant with tool calling
15. GIS dashboard
16. Officer verification workflow
17. Audit trail
18. Unit/integration tests
19. Docker configuration
20. README with complete setup instructions
21. Architecture diagram
22. API documentation
23. Demo script

Build the MVP in a way that a government evaluator can clearly see:
**the problem → the data → the computation → the recommendation → the evidence → the human decision.**