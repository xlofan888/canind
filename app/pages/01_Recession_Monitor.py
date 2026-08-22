import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import streamlit as st
import plotly.express as px
from src.database.repository import read_observations, read_scores

st.title("🔴 Recession Monitor")
df = read_observations()
scores = read_scores(100)

if not scores.empty:
    fig = px.line(scores.sort_values("calculated_at"), x="calculated_at", y="recession_risk",
                  markers=True, title="Recession Risk History")
    st.plotly_chart(fig, use_container_width=True)

for indicator in ["real_gdp", "unemployment", "job_vacancies", "pmi_composite", "retail_sales", "housing_starts"]:
    d = df[df.indicator_id == indicator].sort_values("reference_period")
    if not d.empty:
        fig = px.line(d, x="reference_period", y="value", markers=True, title=indicator.replace("_"," ").title())
        st.plotly_chart(fig, use_container_width=True)
