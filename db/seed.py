import sqlite3, os, json

os.makedirs('data/structured', exist_ok=True)
json_path = 'data/structured/watershed_data.json'

if not os.path.exists(json_path):
    print(f"Error: {json_path} not found. Run fetch_watershed_data.py first.")
    exit()

with open(json_path) as f:
    d = json.load(f)

print(f"Loaded watershed: {d['name']} ({d['region']})")

conn = sqlite3.connect('data/structured/watersheds.db')
c = conn.cursor()

with open('db/schema.sql') as f:
    c.executescript(f.read())

c.execute('DELETE FROM watersheds')

c.execute('''
    INSERT INTO watersheds (
        name, lat, lon, region,
        riparian_soil_ph, riparian_soc_pct, clay_pct, moisture,
        rainfall_mm, temp_c,
        water_ph, turbidity_ntu, dissolved_oxygen_mgl,
        upstream_land_use, deforestation_rate, pollution_level,
        aquatic_species_richness, riparian_buffer_width_m, habitat_diversity
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    d['name'], d['lat'], d['lon'], d['region'],
    d['riparian_soil_ph'], d['riparian_soc_pct'], d['clay_pct'], d['moisture'],
    d['rainfall_mm'], d['temp_c'],
    d['water_ph'], d['turbidity_ntu'], d['dissolved_oxygen_mgl'],
    d['upstream_land_use'], d['deforestation_rate'], d['pollution_level'],
    d['aquatic_species_richness'], d['riparian_buffer_width_m'], d['habitat_diversity']
))

conn.commit()
conn.close()
print("✅ Watershed database seeded successfully.")