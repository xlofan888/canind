"""CMHC adapter. Uses a CSV URL supplied by CANIND_CMHC_CSV until a stable public API key/feed is configured.
No fabricated fallback values are emitted.
"""
import os, pandas as pd

def collect_housing_starts():
    url=os.getenv('CANIND_CMHC_CSV')
    if not url: return None
    df=pd.read_csv(url)
    # Configurable lightweight convention for a verified CMHC export.
    period_col=os.getenv('CANIND_CMHC_PERIOD_COLUMN','REF_DATE'); value_col=os.getenv('CANIND_CMHC_VALUE_COLUMN','VALUE')
    if period_col not in df or value_col not in df: raise ValueError('CMHC CSV missing configured columns')
    x=df.dropna(subset=[period_col,value_col]).sort_values(period_col).iloc[-1]
    return {'indicator_id':'housing_starts','reference_period':str(x[period_col]),'release_date':str(x[period_col]),'value':float(x[value_col]),'unit':'units','source':'CMHC','data_status':'LIVE','source_url':url}
