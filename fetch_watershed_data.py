import requests
import json
import os
from datetime import datetime

LAT = 26.5
LON = 80.5
START_DATE = "20230101"
END_DATE = "20231231"
OUTPUT_PATH = "data/structured/watershed_data.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


def fetch_soil(lat, lon):
    print(f"\n[1/4] Fetching riparian soil data for lat={lat}, lon={lon}...")
    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query"
        f"?lon={lon}&lat={lat}"
        f"&property=phh2o&property=soc&property=clay"
        f"&depth=0-5cm&value=mean"
    )
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        ph, soc, clay = None, None, None
        for layer in data['properties']['layers']:
            val = layer['depths'][0]['values']['mean']
            if val is None:
                continue
            if layer['name'] == 'phh2o':
                ph = round(val / 10.0, 2)
            elif layer['name'] == 'soc':
                soc = round(val / 100.0, 2)
            elif layer['name'] == 'clay':
                clay = round(val / 10.0, 1)
        ph = ph or 7.0
        soc = soc or 1.0
        clay = clay or 25.0
        print(f"  ✅ Riparian Soil pH: {ph}, SOC: {soc}%, Clay: {clay}%")
        return {"riparian_soil_ph": ph, "riparian_soc_pct": soc, "clay_pct": clay}
    except Exception as e:
        print(f"  ❌ SoilGrids error: {e}")
        return {"riparian_soil_ph": 7.0, "riparian_soc_pct": 1.0, "clay_pct": 25.0}


def fetch_climate(lat, lon, start, end):
    print(f"\n[2/4] Fetching climate data from NASA POWER...")
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOTCORR,T2M"
        f"&community=AG&longitude={lon}&latitude={lat}"
        f"&start={start}&end={end}&format=JSON"
    )
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        params = r.json()['properties']['parameter']
        rain = [v for v in params['PRECTOTCORR'].values() if v is not None and v > -900]
        temp = [v for v in params['T2M'].values() if v is not None and v > -900]
        total_rain = round(sum(rain), 1) if rain else 600.0
        avg_temp = round(sum(temp) / len(temp), 1) if temp else 25.0
        print(f"  ✅ Rainfall: {total_rain} mm/yr, Temp: {avg_temp} °C")
        return {"rainfall_mm": total_rain, "temp_c": avg_temp}
    except Exception as e:
        print(f"  ❌ NASA POWER error: {e}")
        return {"rainfall_mm": 600.0, "temp_c": 25.0}


def fetch_water_quality(rainfall_mm, temp_c):
    print(f"\n[3/4] Deriving water quality metrics...")
    turbidity = round(max(2.0, 60.0 - (rainfall_mm / 20)), 1)
    do = round(min(12.0, 5.0 + (rainfall_mm / 200)), 1)
    water_ph = round(6.5 + (temp_c / 40), 2)
    print(f"  ✅ Water pH: {water_ph}, Turbidity: {turbidity} NTU, DO: {do} mg/L")
    return {"water_ph": water_ph, "turbidity_ntu": turbidity, "dissolved_oxygen_mgl": do}


def classify_region(temp_c, rainfall_mm):
    if temp_c > 25 and rainfall_mm < 500:
        return "semi-arid"
    elif temp_c > 25 and rainfall_mm >= 1000:
        return "tropical"
    elif temp_c < 15:
        return "temperate"
    return "subtropical"


def classify_moisture(rainfall_mm):
    if rainfall_mm < 500:
        return "low"
    elif rainfall_mm < 1000:
        return "medium"
    return "high"


def estimate_riparian_buffer(land_use):
    if 'forest' in land_use:
        return 25.0
    elif 'agri' in land_use:
        return 5.0
    return 10.0


def main():
    print("=" * 60)
    print("WATERSHED STRUCTURED DATA FETCHER")
    print("=" * 60)

    soil = fetch_soil(LAT, LON)
    climate = fetch_climate(LAT, LON, START_DATE, END_DATE)
    water = fetch_water_quality(climate['rainfall_mm'], climate['temp_c'])

    region = classify_region(climate['temp_c'], climate['rainfall_mm'])
    moisture = classify_moisture(climate['rainfall_mm'])

    upstream_land_use = "agricultural"
    aquatic_species = 8
    pollution = "high"
    deforestation = "medium"
    habitat = "low"
    buffer_width = estimate_riparian_buffer(upstream_land_use)

    merged = {
        "name": "Sample Watershed",
        "lat": LAT,
        "lon": LON,
        "region": region,
        "riparian_soil_ph": soil['riparian_soil_ph'],
        "riparian_soc_pct": soil['riparian_soc_pct'],
        "clay_pct": soil['clay_pct'],
        "moisture": moisture,
        "rainfall_mm": climate['rainfall_mm'],
        "temp_c": climate['temp_c'],
        "water_ph": water['water_ph'],
        "turbidity_ntu": water['turbidity_ntu'],
        "dissolved_oxygen_mgl": water['dissolved_oxygen_mgl'],
        "upstream_land_use": upstream_land_use,
        "deforestation_rate": deforestation,
        "pollution_level": pollution,
        "aquatic_species_richness": aquatic_species,
        "riparian_buffer_width_m": buffer_width,
        "habitat_diversity": habitat,
        "fetched_at": datetime.now().isoformat()
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(merged, f, indent=2)

    print("\n" + "=" * 60)
    print(f"✅ Watershed data saved to {OUTPUT_PATH}")
    print("=" * 60)
    print(json.dumps(merged, indent=2))


if __name__ == "__main__":
    main()