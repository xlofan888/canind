from collections import Counter

def summarize(rows):
    c=Counter(str(r.get('data_status','UNKNOWN')).upper() for r in rows)
    return {'LIVE':c['LIVE'],'CACHED':c['CACHED'],'DEMO':c['DEMO'],'UNKNOWN':c['UNKNOWN'],'total':sum(c.values())}
