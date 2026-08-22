import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
import streamlit as st
from src.database.repository import read_observations

st.title("📊 All Indicators")
df = read_observations()
st.dataframe(df.sort_values(["indicator_id","reference_period"]), use_container_width=True, hide_index=True)
