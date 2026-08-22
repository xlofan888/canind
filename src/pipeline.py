import os,json,yaml
from pathlib import Path
from datetime import datetime,timezone
import pandas as pd
from src.database.repository import init_db,upsert_observations,save_scores,read_observations
from src.collectors.demo import demo_frame
from src.collectors.bank_of_canada import get_usd_cad
from src.transforms.scoring import calculate_recession_risk,calculate_momentum,calculate_breadth,calculate_transition

def load_yaml(path):
 with open(path,encoding='utf-8') as f:return yaml.safe_load(f)
def boc_rows():
 try:
  payload=get_usd_cad('2015-01-01'); out=[]
  for obs in payload.get('observations',[]):
   v=obs.get('FXUSDCAD',{}).get('v')
   if v is not None: out.append({'indicator_id':'cad_usd','reference_period':obs.get('d'),'release_date':obs.get('d'),'value':float(v),'unit':'CAD per USD','source':'Bank of Canada Valet','vintage_id':datetime.now(timezone.utc).date().isoformat(),'data_status':'LIVE','source_url':'https://www.bankofcanada.ca/valet/docs'})
  return out
 except Exception:return []
def run(mode=None):
 init_db(); mode=(mode or os.getenv('CANIND_MODE','HYBRID')).upper(); rows=[]
 if mode in ('LIVE','HYBRID'): rows.extend(boc_rows())
 # Until each StatsCan vector is explicitly configured and validated, keep them clearly DEMO.
 if mode=='DEMO' or mode=='HYBRID': rows.extend(demo_frame().to_dict('records'))
 if not rows: rows.extend(demo_frame().to_dict('records'))
 upsert_observations(rows); all_data=read_observations(); thresholds=load_yaml('config/thresholds.yaml')['recession']
 scores={'recession_risk':calculate_recession_risk(all_data,thresholds),'transition_score':calculate_transition(all_data),'momentum_score':calculate_momentum(all_data),'breadth_score':calculate_breadth(all_data)}
 save_scores(scores)
 Path('data/snapshots').mkdir(parents=True,exist_ok=True)
 Path('data/snapshots/latest.json').write_text(json.dumps({'updated_at':datetime.now(timezone.utc).isoformat(),'mode':mode,'scores':scores},indent=2))
 return scores
if __name__=='__main__': print(run())
