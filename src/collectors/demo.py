from datetime import date
import pandas as pd

# Demo values make the dashboard immediately runnable before all official
# series IDs are mapped. They are clearly marked as DEMO in the UI.
def demo_frame():
    periods = pd.period_range("2025-01", "2026-08", freq="M").astype(str)
    data = {
        "real_gdp": [0.2,0.3,0.1,0.2,0.1,0.0,-0.1,0.2,0.2,0.1,0.0,0.2,0.1,0.2,0.1,0.0,0.2,0.2,0.1,0.2],
        "unemployment": [6.7,6.6,6.5,6.4,6.4,6.5,6.5,6.4,6.3,6.4,6.5,6.6,6.5,6.4,6.3,6.4,6.5,6.4,6.4,6.4],
        "job_vacancies": [1.0,0.5,0.2,-0.5,-1.0,-1.5,-2.0,-1.0,0.0,0.5,1.0,0.5,0.0,-0.5,-1.0,-1.5,-2.0,-1.0,0.0,0.5],
        "pmi_composite": [49.8,50.1,50.3,49.7,49.4,48.9,49.5,50.2,50.5,50.1,49.8,49.5,50.0,50.2,49.8,49.5,49.9,50.1,49.7,49.7],
        "us_exports": [2,1,-1,-2,-1,0,1,-2,-3,-2,-1,0,-2,-4,-3,-5,-6,-7,-8,-8],
        "non_us_exports": [1,1,2,1,2,2,3,2,3,3,2,4,3,4,4,5,5,5,6,7],
        "business_investment": [1.2,1.1,0.8,0.6,0.5,0.4,0.3,0.5,0.7,0.9,0.8,0.7,0.5,0.4,0.2,0.1,0.0,-0.1,-0.2,-0.2],
        "retail_sales": [0.4,0.5,0.2,0.3,0.1,-0.2,0.3,0.4,0.2,0.1,0.3,0.5,0.4,0.2,0.1,0.0,0.3,0.6,0.4,0.2],
        "housing_starts": [2,1,0,-2,-1,-3,-2,0,1,2,0,-1,-2,-3,-1,0,2,1,0,-1],
        "core_cpi": [2.4,2.3,2.2,2.1,2.1,2.2,2.3,2.2,2.1,2.0,2.1,2.2,2.3,2.4,2.5,2.4,2.3,2.2,2.2,2.2],
    }
    rows = []
    for i, p in enumerate(periods):
        for k, vals in data.items():
            rows.append({
                "indicator_id": k,
                "reference_period": p,
                "release_date": str(date.today()),
                "value": vals[i],
                "unit": "percent" if k not in ("pmi_composite",) else "index",
                "source": "DEMO",
                "vintage_id": "demo-v0.1",
            })
    return pd.DataFrame(rows)
