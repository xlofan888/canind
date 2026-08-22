# CANIND v0.2
Canada Economic Command Center.

## What changed in v0.2
- HYBRID / LIVE / DEMO pipeline modes
- Bank of Canada Valet live USD/CAD ingestion
- Observation-level provenance: LIVE / CACHED / DEMO
- Data freshness summary
- What Changed table
- Snapshot metadata
- Safer scheduled GitHub Actions update

## Run locally
```bash
pip install -r requirements.txt
CANIND_MODE=HYBRID python -m src.pipeline
streamlit run app/dashboard.py
```

## Important production rule
Statistics Canada indicators remain DEMO until each vector/table mapping is explicitly configured and validated. The dashboard labels their provenance and does not present them as live official observations.
