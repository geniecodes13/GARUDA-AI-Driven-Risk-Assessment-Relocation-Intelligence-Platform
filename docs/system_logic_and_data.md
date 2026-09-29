# GARUDA system logic and data model

This document explains the logic used by the current GARUDA MVP and clarifies which parts are real, which parts are prototype logic, and which data is dummy or external.

## 1. What the system is doing

The current platform is a decision-support dashboard for disaster relocation planning. It is built around a single workflow:

1. Select a region, district, block, and habitation.
2. Estimate hazard exposure.
3. Estimate vulnerability.
4. Combine both into a risk score.
5. Rank relocation priority.
6. Find candidate relocation sites.
7. Check carrying capacity and limiting factors.
8. Review resource sufficiency.
9. Run a what-if relocation scenario.
10. Explain the recommendation through a constrained AI assistant.

This is implemented mainly in:

- `streamlit_app.py` — UI and dashboard orchestration
- `backend/data/demo_data.py` — all demo records used by the system
- `backend/engines/` — deterministic scoring and recommendation logic
- `backend/ai_assistant.py` — natural-language explanation layer

## 2. Core logic in the system

### 2.1 Hazard assessment logic

Each habitation contains normalized values between 0 and 1 for:

- flood exposure
- landslide exposure
- historical disaster impact
- accessibility risk

The platform calculates a hazard score using a weighted formula, for example:

- 0.40 × flood exposure
- 0.35 × landslide exposure
- 0.25 × historical disaster impact

The project makes this configurable and labels it as a prototype model.

In the code, the hazard engine calculates a normalized component score and a final score in the 0–100 range. The UI then displays each component individually so the user can see which driver is pushing the score up.

### 2.2 Vulnerability logic

Each habitation also contains vulnerability indicators such as:

- population vulnerability
- housing vulnerability
- healthcare accessibility risk
- road accessibility risk
- evacuation difficulty
- critical infrastructure risk

The system combines these into a vulnerability index using weighted coefficients similar to:

- 0.30 × population vulnerability
- 0.20 × housing vulnerability
- 0.20 × healthcare accessibility risk
- 0.15 × road accessibility risk
- 0.15 × evacuation difficulty

The result is again normalized and then displayed as a scored component breakdown.

### 2.3 Risk calculation logic

The risk engine uses the formula:

- Risk = Hazard Exposure × Vulnerability

This is converted to a score on a 0–100 scale. The system then classifies it into bands:

- 0–20: Low
- 20–40: Moderate
- 40–60: High
- 60–80: Very High
- 80–100: Critical

The implementation also returns:

- risk score
- risk class
- confidence level
- major contributing factors
- data freshness fields
- explanation text

Important: the platform does not claim legal status as a government red zone. It instead uses language like “AI-assessed high-risk zone” and “Candidate Red Zone — requires authority verification”.

### 2.4 Relocation priority logic

The relocation priority engine evaluates:

- risk score
- population vulnerability
- historical disaster impact
- exposed population
- evacuation difficulty

This produces a priority label such as:

- IMMEDIATE
- SHORT-TERM
- MEDIUM-TERM
- MONITOR

The system does not display only a score; it also includes an explanation describing why that habitation is prioritized. This matches the PRD requirement for explainability and actionable decision support.

### 2.5 Safe-site discovery logic

The site matching logic evaluates candidate relocation locations by applying hard and soft constraints.

Hard constraints reject a site if it is:

- inside a high-risk flood area
- inside a high-risk landslide area
- environmentally restricted
- poorly connected by roads
- lacking sufficient usable land

Soft constraints are then used to rank the remaining sites based on:

- distance from the original habitation
- road accessibility
- healthcare access
- school access
- water availability
- infrastructure quality
- environmental suitability
- residual hazard
- development requirement

The current prototype uses a demo set of candidate sites and synthetic capacity values.

### 2.6 Effective carrying capacity logic

The current model does not compute capacity as a simple land-area-per-person rule. Instead, it computes capacity across multiple dimensions:

- land capacity
- water capacity
- road capacity
- healthcare capacity
- school capacity
- environmental capacity
- shelter capacity

Then it uses the minimum value as the effective carrying capacity:

- Effective Capacity = MIN(Land, Water, Road, Healthcare, School, Environmental, Shelter)

This is an important design feature because it exposes the limiting factor. The UI highlights which infrastructure dimension is the bottleneck.

### 2.7 Relocation matching logic

The system assigns populations to candidate sites by considering:

- site capacity
- safety constraints
- maximum relocation distance
- infrastructure constraints
- residual risk

The objective is to minimize:

- relocation distance
- infrastructure deficit
- residual risk
- development cost

while keeping allocation within site capacity. This logic is represented in a prototype scenario engine instead of a full live optimization solver.

### 2.8 What-if simulation logic

The scenario simulator lets an authority change:

- population to relocate
- percentage relocated
- candidate sites
- maximum relocation distance
- infrastructure investment
- risk threshold

It then recalculates:

- site allocation
- remaining capacity
- infrastructure gap
- total relocation distance
- estimated resource gap

This is a decision-support layer, not a legal or operational final recommendation.

### 2.9 AI assistant logic

The AI component is intentionally constrained.

It is not allowed to independently compute risk. Instead, it works in this chain:

- User question
- AI query interpretation
- Structured GIS/risk query against the internal data model
- Verified numerical output from the deterministic engine
- AI explanation using the verified answer

This prevents the assistant from inventing numbers. It is meant for explanation and natural-language summarization.

### 2.10 Frontend map logic

The dashboard uses a Leaflet/Folium map as a visual layer over the synthetic dataset. It displays:

- habitation points
- candidate site points
- risk color coding
- site status information
- interactive popups/tooltips

This is a map-based visualization layer; it is not a live geospatial dataset ingestion pipeline.

## 3. Data: dummy or fetched?

### 3.1 Current status: the data is mostly dummy prototype data

The current project uses synthetic demo data stored in:

- `backend/data/demo_data.py`

This file contains arrays such as:

- `HABITATIONS`
- `CANDIDATE_SITES`
- `RESOURCE_INVENTORY`

These records include sample populations, coordinates, vulnerability scores, site capacities, and inventory counts. They are intentionally constructed to simulate a pilot Uttarakhand dataset.

### 3.2 The data is not connected to a live GIS source right now

At the moment, the system does not fetch real hazard layers, population tables, road networks, or satellite-derived GIS datasets from live APIs or government data sources.

The following are not connected in the current app:

- live PostGIS database queries
- external flood or landslide datasets
- real census APIs
- actual OSM road network ingestion
- real remote sensing processing

### 3.3 What is external and what is local

There are two different kinds of data involved:

1. Real network dependency for canvas/map display
   - The basemap itself is rendered through a public OpenStreetMap tile source.
   - This is only for the map background layer and is not the actual hazard dataset.
   - It is not the source of the decision logic.

2. Local synthetic pilot records
   - all habitation and site locations used in scoring are handcrafted in the Python data module
   - resource inventory data is also synthetic and illustrative

### 3.4 Schema and database status

The repo also includes a Postgres/PostGIS schema stub in:

- `database/postgres_schema.sql`

This is a future-ready schema design for storing:

- habitations
- relocation sites
- resource inventory
- risk assessments
- priority outputs
- field reports

But the current app is not using this database live. It is a design template for later integration.

### 3.5 Practical conclusion

The current GARUDA platform is a working prototype MVP for demonstration and logic validation. It is not a production-grade operational system connected to official datasets.

The logical engine is real and deterministic, but the data is synthetic and intentionally demo-only.

## 4. Why this is appropriate for an MVP

This is the right structure for a hackathon and prototype system because it allows the team to demonstrate:

- real scoring logic
- clear risk interpretation
- explainable AI interactions
- site feasibility assessment
- relocation planning workflow

without pretending to be an official government data product.

## 5. Recommended next step

To turn this into a production-ready platform, the next step would be:

- connect a real PostGIS database
- ingest official flood and landslide layers
- integrate OSM or government road network data
- replace synthetic site and vulnerability values with field-validated records
- add authentication and audit logs for authority workflows

That would move the system from a working demo to a real decision-support platform for disaster resilience planning.
