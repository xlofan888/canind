import streamlit as st

st.title("🔎 Data Sources")

st.markdown("""
### Primary official sources

- **Statistics Canada Web Data Service (WDS)** — GDP, employment, unemployment, trade, retail sales, CPI, investment and other official statistics.
- **Bank of Canada Valet API** — exchange rates, monetary and financial statistics.

### v0.1 status

| Source | Status |
|---|---|
| Statistics Canada WDS | Connector included; vector mapping pending |
| Bank of Canada Valet | Connector included |
| CMHC | Planned |
| CREA | Planned |
| S&P Global PMI | Planned / source-specific access |

**Important:** DEMO data is explicitly labelled and must not be interpreted as official observations.
""")
