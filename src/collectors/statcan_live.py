from pathlib import Path
import yaml
from src.collectors.statcan_wds import collect_latest, MappingError
from src.validation.mapping import validate_result
from src.validation.values import validate_range

def load_specs(path='src/mappings/indicator_specs.yaml'):
    return yaml.safe_load(Path(path).read_text()) or {}

def collect_all(strict=False):
    rows=[]; errors=[]
    for indicator_id,spec in load_specs().items():
        try:
            row=collect_latest(spec); validate_result(indicator_id,row); validate_range(indicator_id,row['value'])
            row['indicator_id']=indicator_id; row['unit']=spec.get('unit','')
            rows.append(row)
        except Exception as e:
            errors.append({'indicator_id':indicator_id,'error':str(e)})
            if strict: raise
    return rows,errors
