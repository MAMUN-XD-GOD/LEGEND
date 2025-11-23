from datetime import datetime

def normalize(c):
    n = {}
    ts = c.get('ts')
    if isinstance(ts, (int,float)):
        n['ts'] = int(ts)
    else:
        try:
            n['ts'] = int(datetime.fromisoformat(ts).timestamp())
        except:
            n['ts'] = None
    n['open'] = float(c.get('open',0))
    n['high'] = float(c.get('high',0))
    n['low'] = float(c.get('low',0))
    n['close'] = float(c.get('close',0))
    n['volume'] = float(c.get('volume',0))
    return n

def normalize_list(lst):
    return [normalize(c) for c in lst]
