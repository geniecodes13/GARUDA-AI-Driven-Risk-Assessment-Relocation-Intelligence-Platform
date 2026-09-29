# GARUDA — AI-Driven Risk Assessment & Relocation Intelligence Platform

GARUDA is a prototype decision-support platform for AI-driven proactive disaster relocation planning in Uttarakhand. The MVP combines deterministic GIS logic, vulnerability analysis, relocation prioritization, site suitability, resource intelligence, and an explainable AI-facing query layer.

> Prototype pilot — methodology can be extended to additional regions and hazards.

## Core workflow

1. Select region, district, block, and habitation.
2. Score hazard exposure and vulnerability.
3. Compute overall risk; classify as low, moderate, high, very high, or critical.
4. Rank relocation priority.
5. Discover candidate safe relocation sites.
6. Evaluate capacity and limiting factors.
7. Check resource sufficiency and relocation feasibility.
8. Run a what-if simulation.
9. Explain recommendation with audited drivers and data freshness.

## Project structure

- `streamlit_app.py` — local decision cockpit UI
- `backend/` — analytics, data model, API, and AI assistant logic
- `database/postgres_schema.sql` — PostGIS/PostgreSQL schema draft
- `docs/architecture.md` — system diagram
- `docs/demo_script.md` — live demonstration steps
- `tests/` — unit tests for risk and capacity logic

## Demo data status

The MVP uses synthetic prototype data for the pilot region. It is explicitly demo-only and should not be presented as official government data.

## Local setup

```bash
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Docker run

```bash
docker build -t garuda .
docker run -p 8501:8501 garuda
```

## API docs

The lightweight FastAPI app is available in `backend/api/main.py` and exposes health and summary endpoints under `/docs` when launched locally.

```bash
uvicorn backend.api.main:app --reload --port 8000
```

Then open: http://localhost:8000/docs

## Technology alignment

This MVP follows the streamlit-first deployment instruction and keeps the analytical engine modular so it can later be connected to PostGIS-backed datasets and external GIS sources.

## Key deliverables included

- hazard scoring engine
- vulnerability engine
- risk engine
- relocation priority engine
- safe-site discovery
- effective carrying capacity logic
- resource feasibility checks
- scenario simulator
- explainability layer
- constrained AI assistant
- test coverage
- PostgreSQL/PostGIS schema
- Docker configuration
