import os,json,yaml
from pathlib import Path
from datetime import datetime,timezone
from src.database.repository import init_db,upsert_observations,save_scores,read_observations
from src.collectors.demo import demo_frame
from src.collectors.bank_of_canada import get_usd_cad
from src.collectors.statcan_live import collect_all
from src.collectors.cmhc import collect_housing_starts
from src.services.data_status import summarize
from src.transforms.scoring import calculate_recession_risk,calculate_momentum,calculate_breadth,calculate_transition

def load_yaml(path):
 with open(path,encoding='utf-8') as f:return yaml.safe_load(f)
def boc_rows():
 try:
  p=get_usd_cad('2015-01-01'); out=[]
  for o in p.get('observations',[]):
   v=o.get('FXUSDCAD',{}).get('v')
   if v is not None: out.append({'indicator_id':'cad_usd','reference_period':o.get('d'),'release_date':o.get('d'),'value':float(v),'unit':'CAD per USD','source':'Bank of Canada Valet','vintage_id':datetime.now(timezone.utc).date().isoformat(),'data_status':'LIVE','source_url':'https://www.bankofcanada.ca/valet/docs'})
  return out
 except Exception:return []
def _demo_rows(existing_ids):
 return [r for r in demo_frame().to_dict('records') if r['indicator_id'] not in existing_ids]
def run(mode=None):
 init_db(); mode=(mode or os.getenv('CANIND_MODE','HYBRID')).upper(); rows=[]; errors=[]
 if mode in ('LIVE','HYBRID'):
  live,errors=collect_all(strict=(mode=='LIVE')); rows.extend(live); rows.extend(boc_rows())
  try:
   h=collect_housing_starts()
   if h: rows.append(h)
  except Exception as e: errors.append({'indicator_id':'housing_starts','error':str(e)})
 if mode=='DEMO': rows=demo_frame().to_dict('records')
 elif mode=='HYBRID':
  ids={r['indicator_id'] for r in rows}; fallback=_demo_rows(ids)
  for r in fallback: r['data_status']='DEMO'; rows.append(r)
 if mode=='LIVE' and not rows: raise RuntimeError('LIVE mode produced no verified observations')
 if not rows: rows=demo_frame().to_dict('records')
 upsert_observations(rows); all_data=read_observations(); thresholds=load_yaml('config/thresholds.yaml')['recession']
 scores={'recession_risk':calculate_recession_risk(all_data,thresholds),'transition_score':calculate_transition(all_data),'momentum_score':calculate_momentum(all_data),'breadth_score':calculate_breadth(all_data)}
 save_scores(scores); Path('data/snapshots').mkdir(parents=True,exist_ok=True)
 payload={'updated_at':datetime.now(timezone.utc).isoformat(),'mode':mode,'scores':scores,'data_status':summarize(rows),'mapping_errors':errors}
 Path('data/snapshots/latest.json').write_text(json.dumps(payload,indent=2))
 return scores
if __name__=='__main__': print(run())
