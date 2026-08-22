import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import streamlit as st
import plotly.express as px
from src.database.repository import read_observations

st.title("🌎 Trade & Transition")
df = read_observations()

trade = df[df.indicator_id.isin(["us_exports","non_us_exports"])].copy()
if not trade.empty:
    fig = px.line(trade, x="reference_period", y="value", color="indicator_id", markers=True,
                  title="US vs Non-US Export Growth")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Transition logic

The production version will calculate:

**Non-US Export Replacement Ratio = growth in non-US exports / decline in US exports**

This is intended to answer whether trade diversification is actually replacing lost US demand.
""")
