import os
import requests
from datetime import datetime, timezone

BASE = "https://www150.statcan.gc.ca/t1/wds/rest"
UA = os.getenv("CANIND_USER_AGENT", "canind/0.1")

def get_vector_latest(vector_id: int, periods: int = 60):
    url = f"{BASE}/getDataFromVectorByReferencePeriodRange"
    # WDS requires a reference period range; this helper intentionally uses
    # a small fallback window and can be replaced by a vector-specific range.
    params = {"vectorIds": str(vector_id), "startRefPeriod": "2015-01", "endReferencePeriod": "2030-12"}
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()

def get_changed_series():
    r = requests.get(f"{BASE}/getChangedSeriesList", headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()

def normalize_wds_points(payload, indicator_id, unit=""):
    rows = []
    obj = payload.get("object", payload)
    if isinstance(obj, dict):
        obj = obj.get("vectorDataPoint", obj.get("data", []))
    if not isinstance(obj, list):
        return rows
    for p in obj:
        value = p.get("value")
        if value is None:
            continue
        ref = p.get("refPer") or p.get("refper") or p.get("referencePeriod")
        rows.append({
            "indicator_id": indicator_id,
            "reference_period": str(ref),
            "release_date": p.get("releaseTime") or p.get("releaseDate"),
            "value": float(value),
            "unit": unit,
            "source": "Statistics Canada WDS",
            "vintage_id": p.get("issueDate") or datetime.now(timezone.utc).date().isoformat(),
        })
    return rows
