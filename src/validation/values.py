RANGES={'unemployment':(0,100),'cpi':(0,1000),'job_vacancies':(0,1e8),'retail_sales':(0,1e13),'business_investment':(0,1e13),'building_permits':(0,1e13),'real_gdp':(0,1e14)}
def validate_range(indicator_id,value):
    lo,hi=RANGES.get(indicator_id,(-float('inf'),float('inf')))
    if not lo <= float(value) <= hi: raise ValueError(f'{indicator_id}: {value} outside [{lo},{hi}]')
    return True
