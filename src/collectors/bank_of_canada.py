import requests
import pandas as pd
from io import StringIO

BASE = "https://www.bankofcanada.ca/valet"

def get_series(series_name: str, start_date="2015-01-01"):
    url = f"{BASE}/observations/{series_name}/json"
    r = requests.get(
        url,
        params={"start_date": start_date},
        headers={"User-Agent": "canind/0.1"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

def get_usd_cad(start_date="2015-01-01"):
    # Bank of Canada Valet exchange-rate series.
    return get_series("FXUSDCAD", start_date=start_date)
