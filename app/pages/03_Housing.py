import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import streamlit as st
import plotly.express as px
from src.database.repository import read_observations

st.title("🏠 Housing")
df = read_observations()
d = df[df.indicator_id == "housing_starts"].sort_values("reference_period")
if not d.empty:
    st.plotly_chart(px.line(d, x="reference_period", y="value", markers=True,
                            title="Housing Starts Growth"), use_container_width=True)
st.caption("CMHC/CREA production connectors are reserved for the next data-source integration pass.")
