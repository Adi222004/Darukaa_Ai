def generate_recommendations(slots):
    recommendations = []

    water_ph = slots.get('water_ph', 7.0)
    turbidity = slots.get('turbidity_ntu', 10.0)
    do = slots.get('dissolved_oxygen_mgl', 6.0)
    upstream = slots.get('upstream_land_use', 'unknown').lower()
    aquatic_species = slots.get('aquatic_species_richness', 20)
    pollution = slots.get('pollution_level', 'medium')
    buffer_width = slots.get('riparian_buffer_width_m', 0)
    rainfall = slots.get('rainfall_mm', 800)
    region = slots.get('region', 'unknown').lower()

    # Rule 1: Low DO + High Turbidity + Agricultural Upstream
    if do < 5.0 and turbidity > 20 and 'agri' in upstream:
        recommendations.append({
            "recommendation": "Construct constructed wetlands for nutrient runoff filtration",
            "why": "Constructed wetlands reduce nitrogen loading by 40-60% and phosphorus by 30-50%, raising dissolved oxygen levels and restoring aquatic habitat.",
            "metrics_improved": ["dissolved oxygen", "turbidity", "aquatic species richness"],
            "time_horizon": "medium (2-3 years)",
            "confidence": "High",
            "evidence": [{"source": "UNEP", "year": 2021, "url": "https://www.unep.org"}]
        })

    # Rule 2: Narrow Riparian Buffer + Low Species Richness
    if buffer_width < 10 and aquatic_species < 15:
        recommendations.append({
            "recommendation": "Restore 30-meter riparian buffer strips with native vegetation",
            "why": "Riparian buffers of 30m width reduce sediment load by 70-90% and support 2-3x more aquatic macroinvertebrate taxa.",
            "metrics_improved": ["turbidity", "aquatic species richness", "water temperature"],
            "time_horizon": "long (3-5 years)",
            "confidence": "High",
            "evidence": [{"source": "IUCN", "year": 2020, "url": "https://iucn.org"}]
        })

    # Rule 3: Acidic Water + High Pollution + Low Rainfall
    if water_ph < 6.0 and pollution == 'high' and rainfall < 700:
        recommendations.append({
            "recommendation": "Install limestone channel beds and reduce upstream industrial discharge",
            "why": "Limestone neutralizes acidic waters (raising pH by 0.5-1.5 units) while reducing industrial inputs prevents further acidification.",
            "metrics_improved": ["water pH", "dissolved oxygen", "aquatic species survival"],
            "time_horizon": "short (6-12 months)",
            "confidence": "Medium",
            "evidence": [{"source": "Ramsar", "year": 2018, "url": "https://www.ramsar.org"}]
        })

    # Rule 4: Semi-arid + High Turbidity + Low Species
    if region == 'semi-arid' and turbidity > 30 and aquatic_species < 12:
        recommendations.append({
            "recommendation": "Install sand filtration basins and native reed bed plantations",
            "why": "Reed beds trap suspended sediment, reducing turbidity by 50-70% in semi-arid rivers while supporting aquatic invertebrate recovery.",
            "metrics_improved": ["turbidity", "aquatic species richness", "water clarity"],
            "time_horizon": "medium (1-2 years)",
            "confidence": "Medium",
            "evidence": [{"source": "IUCN", "year": 2020, "url": "https://iucn.org"}]
        })

    return recommendations