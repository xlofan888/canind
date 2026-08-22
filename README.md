# CANIND v0.3 — Canada Economic Command Center

## v0.3 production data architecture
- Statistics Canada indicators use full-table WDS/bulk downloads and **dimension-based mappings**.
- Every mapping is validated against the downloaded schema; missing dimensions or unmatched labels fail loudly.
- Values are range-validated before persistence.
- `LIVE` mode never invents demo observations. `HYBRID` fills missing indicators with clearly labelled `DEMO` rows.
- Snapshot metadata records mapping errors and LIVE/CACHED/DEMO counts.

## Modes
```bash
CANIND_MODE=HYBRID python -m src.pipeline
CANIND_MODE=LIVE python -m src.pipeline
CANIND_MODE=DEMO python -m src.pipeline
```

## Important mapping note
StatsCan table schemas and labels can change. `src/mappings/indicator_specs.yaml` is intentionally the single source of truth. Review a failed mapping in `data/snapshots/latest.json`; do not silently change a vector ID to make a test pass.

## CMHC
Set `CANIND_CMHC_CSV` to a verified CMHC CSV export or stable official feed. Until configured, housing starts are not falsely reported as LIVE.

## Run
```bash
pip install -r requirements.txt
pytest -q
CANIND_MODE=HYBRID python -m src.pipeline
streamlit run app/dashboard.py
```
