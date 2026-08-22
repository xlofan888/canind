"""Statistics Canada full-table collector with schema-aware extraction.
Uses the official WDS bulk CSV endpoint. Product IDs are configured, never hard-coded in collectors.
"""
from __future__ import annotations
import io, zipfile, requests, pandas as pd
BASE='https://www150.statcan.gc.ca/n1/en/tbl/csv/{pid}-eng.zip'

class MappingError(RuntimeError): pass

def download_table(pid:int, timeout:int=90)->pd.DataFrame:
    r=requests.get(BASE.format(pid=f'{int(pid):08d}'),timeout=timeout)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        csv=[n for n in z.namelist() if n.lower().endswith('.csv') and 'metadata' not in n.lower()]
        if not csv: raise MappingError(f'No data CSV in Product {pid}')
        with z.open(csv[0]) as f: return pd.read_csv(f,low_memory=False)

def _col(df,name):
    exact={str(c).strip().lower():c for c in df.columns}
    if name.strip().lower() in exact:return exact[name.strip().lower()]
    raise MappingError(f'Missing dimension {name!r}; actual={list(df.columns)}')

def extract_latest(df:pd.DataFrame, filters:dict, value_column='VALUE', period_column='REF_DATE'):
    x=df.copy()
    for dim, expected in (filters or {}).items():
        c=_col(x,dim)
        choices=expected if isinstance(expected,list) else [expected]
        mask=False
        actual=x[c].astype(str).str.strip()
        for choice in choices: mask=mask | actual.eq(str(choice))
        x=x[mask]
        if x.empty: raise MappingError(f'Filter {dim}={choices} returned no rows')
    vc=_col(x,value_column); pc=_col(x,period_column)
    x=x.dropna(subset=[vc,pc]).copy(); x[pc]=x[pc].astype(str)
    x=x.sort_values(pc)
    if x.empty: raise MappingError('No observations after filters')
    row=x.iloc[-1]
    return {'reference_period':str(row[pc]),'value':float(row[vc])}

def collect_latest(spec:dict):
    df=download_table(int(spec['product_id']))
    row=extract_latest(df,spec.get('filters',{}),spec.get('value_column','VALUE'),spec.get('period_column','REF_DATE'))
    row['source']='Statistics Canada'; row['source_url']=BASE.format(pid=f"{int(spec['product_id']):08d}")
    row['data_status']='LIVE'; return row
