import numpy as np
import pandas as pd

def interpolate_score(value, points):
    points = sorted(points, key=lambda x: x[0])
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return float(np.clip(np.interp(value, xs, ys), 0, 100))

def latest_by_indicator(df):
    if df.empty:
        return df
    return (
        df.sort_values(["indicator_id", "reference_period"])
          .groupby("indicator_id", as_index=False)
          .tail(1)
    )

def calculate_recession_risk(df, thresholds):
    latest = latest_by_indicator(df)
    risks = []
    for _, row in latest.iterrows():
        key = row["indicator_id"]
        if key not in thresholds:
            continue
        points = thresholds[key]["points"]
        risk = interpolate_score(float(row["value"]), points)
        risks.append((key, risk))
    weights = {
        "real_gdp": .20,
        "unemployment": .20,
        "job_vacancies": .10,
        "pmi_composite": .15,
        "business_investment": .15,
        "retail_sales": .10,
        "housing_starts": .05,
        "core_cpi": .05,
    }
    valid = [(k, r) for k, r in risks if k in weights]
    if not valid:
        return None
    total_w = sum(weights[k] for k, _ in valid)
    return sum(r * weights[k] for k, r in valid) / total_w

def calculate_momentum(df):
    if df.empty:
        return 0.0
    improving = 0
    worsening = 0
    for k, g in df.groupby("indicator_id"):
        g = g.sort_values("reference_period")
        if len(g) < 2:
            continue
        delta = float(g.iloc[-1]["value"] - g.iloc[-2]["value"])
        # Higher unemployment / CPI are bad; most other indicators are good.
        if k in {"unemployment", "core_cpi", "us_exports"}:
            delta = -delta
        if delta > 0:
            improving += 1
        elif delta < 0:
            worsening += 1
    total = improving + worsening
    return 0.0 if total == 0 else 100 * (improving - worsening) / total

def calculate_breadth(df):
    if df.empty:
        return 50.0
    improving = worsening = total = 0
    for k, g in df.groupby("indicator_id"):
        g = g.sort_values("reference_period")
        if len(g) < 2:
            continue
        delta = float(g.iloc[-1]["value"] - g.iloc[-2]["value"])
        if k in {"unemployment", "core_cpi", "us_exports"}:
            delta = -delta
        total += 1
        if delta > 0: improving += 1
        elif delta < 0: worsening += 1
    return 50.0 if total == 0 else 100 * improving / total

def calculate_transition(df):
    latest = latest_by_indicator(df).set_index("indicator_id")
    scores = []
    if "non_us_exports" in latest.index:
        scores.append(float(np.clip(50 + latest.loc["non_us_exports", "value"] * 4, 0, 100)))
    if "business_investment" in latest.index:
        scores.append(float(np.clip(50 + latest.loc["business_investment", "value"] * 10, 0, 100)))
    if "us_exports" in latest.index:
        # Lower dependency growth is better; this prototype uses the latest change.
        scores.append(float(np.clip(50 - latest.loc["us_exports", "value"] * 3, 0, 100)))
    return float(np.mean(scores)) if scores else 50.0
