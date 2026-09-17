CREATE TABLE IF NOT EXISTS watersheds (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    region TEXT,
    riparian_soil_ph REAL,
    riparian_soc_pct REAL,
    clay_pct REAL,
    moisture TEXT,
    rainfall_mm REAL,
    temp_c REAL,
    water_ph REAL,
    turbidity_ntu REAL,
    dissolved_oxygen_mgl REAL,
    upstream_land_use TEXT,
    deforestation_rate TEXT,
    pollution_level TEXT,
    aquatic_species_richness INTEGER,
    riparian_buffer_width_m REAL,
    habitat_diversity TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    source TEXT,
    year INTEGER,
    url TEXT,
    text TEXT,
    embedding_id TEXT
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY,
    practice TEXT,
    metrics_improved TEXT,
    time_horizon TEXT,
    confidence TEXT,
    evidence TEXT,
    source_ids TEXT
);