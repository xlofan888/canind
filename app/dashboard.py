import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.repository import init_db, read_observations, read_scores
from src.pipeline import run

st.set_page_config(page_title="CANIND", page_icon="🇨🇦", layout="wide")
init_db()

if read_observations().empty:
    run()

df = read_observations()
scores = read_scores(1)

st.title("🇨🇦 CANIND — Canada Economic Command Center")
st.caption("v0.1 • Economic health, recession risk and transition monitor")

if scores.empty:
    run()
    scores = read_scores(1)

s = scores.iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Recession Risk", f"{s.recession_risk:.0f}/100")
c2.metric("Transition Score", f"{s.transition_score:.0f}/100")
c3.metric("Momentum", f"{s.momentum_score:+.0f}")
c4.metric("Breadth", f"{s.breadth_score:.0f}/100")

st.divider()

latest = (
    df.sort_values("reference_period")
      .groupby("indicator_id", as_index=False)
      .tail(1)
      .sort_values("indicator_id")
)

st.subheader("Latest indicators")
st.dataframe(
    latest[["indicator_id","reference_period","value","unit","source"]]
    .rename(columns={"indicator_id":"Indicator","reference_period":"Reference","value":"Value","unit":"Unit","source":"Source"}),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Economic indicators")

selected = st.selectbox(
    "Select indicator",
    sorted(df["indicator_id"].unique()),
    index=0,
)

chart_df = df[df["indicator_id"] == selected].sort_values("reference_period")
fig = px.line(
    chart_df,
    x="reference_period",
    y="value",
    markers=True,
    title=selected.replace("_", " ").title(),
)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "v0.1 includes clearly labelled DEMO observations so the application runs immediately. "
    "The next data-engineering step is mapping and validating each official Statistics Canada "
    "series/vector before treating the live scores as production data."
)

with st.expander("Data provenance"):
    st.write(
        "Statistics Canada WDS and Bank of Canada Valet are the intended primary official "
        "sources. DEMO rows are not official economic observations."
    )
