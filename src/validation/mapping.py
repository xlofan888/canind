from src.collectors.statcan_wds import MappingError

def validate_result(indicator_id,row):
    if row is None: raise MappingError(f'{indicator_id}: no result')
    if not row.get('reference_period'): raise MappingError(f'{indicator_id}: missing reference_period')
    if row.get('value') is None: raise MappingError(f'{indicator_id}: missing value')
    return True
