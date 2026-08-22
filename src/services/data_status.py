import pandas as pd

def status_summary(df: pd.DataFrame):
    if df.empty: return {"live":0,"cached":0,"demo":0,"total":0,"freshness":0}
    s=df.get('data_status', pd.Series('LIVE', index=df.index)).fillna('LIVE').str.upper()
    counts={k:int((s==k).sum()) for k in ['LIVE','CACHED','DEMO']}
    total=len(df); freshness=round(100*(counts['LIVE']+counts['CACHED'])/total,1) if total else 0
    return {**{k.lower():v for k,v in counts.items()},'total':total,'freshness':freshness}
