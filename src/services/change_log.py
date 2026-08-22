import pandas as pd

def latest_changes(df):
    rows=[]
    for k,g in df.groupby('indicator_id'):
        g=g.sort_values('reference_period')
        if len(g)<2: continue
        a,b=g.iloc[-2],g.iloc[-1]
        rows.append({'indicator_id':k,'previous':float(a.value),'current':float(b.value),'delta':float(b.value-a.value),'reference_period':b.reference_period})
    return pd.DataFrame(rows)
