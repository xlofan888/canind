import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st, plotly.express as px
from src.database.repository import init_db,read_observations,read_scores
from src.pipeline import run
from src.services.data_status import status_summary
from src.services.change_log import latest_changes
st.set_page_config(page_title='CANIND',page_icon='🇨🇦',layout='wide');init_db()
if read_observations().empty: run()
df=read_observations(); scores=read_scores(1)
if scores.empty: run();scores=read_scores(1)
s=scores.iloc[0]; stat=status_summary(df)
st.title('🇨🇦 CANIND — Canada Economic Command Center');st.caption('v0.2 • Official-data pipeline with transparent LIVE / CACHED / DEMO provenance')
st.caption(f"Data freshness: {stat['freshness']}% • 🟢 LIVE {stat['live']} • 🟡 CACHED {stat['cached']} • ⚪ DEMO {stat['demo']}")
c1,c2,c3,c4=st.columns(4);c1.metric('Recession Risk',f'{s.recession_risk:.0f}/100');c2.metric('Transition Score',f'{s.transition_score:.0f}/100');c3.metric('Momentum',f'{s.momentum_score:+.0f}');c4.metric('Breadth',f'{s.breadth_score:.0f}/100')
st.divider(); latest=df.sort_values('reference_period').groupby('indicator_id',as_index=False).tail(1).sort_values('indicator_id')
st.subheader('Latest indicators');st.dataframe(latest[['indicator_id','reference_period','value','unit','source','data_status']].rename(columns={'indicator_id':'Indicator','reference_period':'Reference','value':'Value','unit':'Unit','source':'Source','data_status':'Status'}),use_container_width=True,hide_index=True)
st.subheader('What changed?');ch=latest_changes(df)
if not ch.empty: st.dataframe(ch.sort_values('indicator_id'),use_container_width=True,hide_index=True)
selected=st.selectbox('Select indicator',sorted(df.indicator_id.unique())); chart=df[df.indicator_id==selected].sort_values('reference_period');st.plotly_chart(px.line(chart,x='reference_period',y='value',markers=True,title=selected.replace('_',' ').title()),use_container_width=True)
st.info('v0.2 never silently mixes demo and official data: every observation carries a source and status. Add validated Statistics Canada vector IDs in the next mapping phase before promoting those indicators to LIVE.')
