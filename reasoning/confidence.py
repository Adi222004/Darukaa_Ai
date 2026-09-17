def score_confidence(num_sources, data_completeness):
    if num_sources >= 3 and data_completeness > 0.8:
        return "High"
    elif num_sources >= 1 and data_completeness > 0.5:
        return "Medium"
    return "Low"