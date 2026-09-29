CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS administrative_units (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    block VARCHAR(100) NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326)
);

CREATE TABLE IF NOT EXISTS habitations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    block VARCHAR(100),
    population INTEGER,
    geom GEOMETRY(Point, 4326),
    flood_exposure NUMERIC(5,3),
    landslide_exposure NUMERIC(5,3),
    historical_impact NUMERIC(5,3),
    accessibility_risk NUMERIC(5,3),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS population_profiles (
    id SERIAL PRIMARY KEY,
    habitation_id INTEGER REFERENCES habitations(id),
    population INTEGER,
    children_percent NUMERIC(5,3),
    elderly_percent NUMERIC(5,3),
    vulnerable_groups NUMERIC(5,3),
    data_year INTEGER
);

CREATE TABLE IF NOT EXISTS candidate_sites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    geom GEOMETRY(Polygon, 4326),
    safe_status VARCHAR(20),
    distance_km NUMERIC(8,2),
    site_capacity INTEGER,
    water_capacity INTEGER,
    healthcare_capacity INTEGER,
    shelter_capacity INTEGER
);

CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,
    resource_type VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    total_quantity INTEGER,
    available_quantity INTEGER,
    deployed_quantity INTEGER,
    status VARCHAR(50),
    last_updated TIMESTAMP DEFAULT NOW(),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS resource_allocations (
    id SERIAL PRIMARY KEY,
    resource_id INTEGER REFERENCES resources(id),
    target_type VARCHAR(50),
    target_id INTEGER,
    quantity INTEGER,
    allocated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id SERIAL PRIMARY KEY,
    habitation_id INTEGER REFERENCES habitations(id),
    hazard_score NUMERIC(5,3),
    vulnerability_score NUMERIC(5,3),
    overall_risk NUMERIC(5,3),
    risk_class VARCHAR(20),
    confidence NUMERIC(5,3),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS priority_assessments (
    id SERIAL PRIMARY KEY,
    habitation_id INTEGER REFERENCES habitations(id),
    priority_level VARCHAR(20),
    reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS field_reports (
    id SERIAL PRIMARY KEY,
    habitation_id INTEGER REFERENCES habitations(id),
    officer_name VARCHAR(100),
    gps_location GEOMETRY(Point, 4326),
    road_condition VARCHAR(50),
    water_availability VARCHAR(50),
    infrastructure_status TEXT,
    observations TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_habitations_geom ON habitations USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_candidate_sites_geom ON candidate_sites USING GIST (geom);
