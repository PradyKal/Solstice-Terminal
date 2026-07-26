"""Alpaca execution — bracket orders, trailing stops, market-hours gating."""
import requests, time, json

def submit_bracket(base, headers, symbol, qty, limit_p, stop_p, profit_p):
    body = {'symbol':symbol,'qty':str(int(qty)),'side':'buy','type':'limit',
            'limit_price':f'{limit_p:.2f}','time_in_force':'day','order_class':'bracket',
            'take_profit':{'limit_price':f'{profit_p:.2f}'},
            'stop_loss':{'stop_price':f'{stop_p:.2f}','limit_price':f'{stop_p*0.997:.2f}'},
            'client_order_id':f'sol-{int(time.time())}-{symbol}'}
    r = requests.post(f'{base}/orders', headers=headers, data=json.dumps(body), timeout=12)
    return r.json() if r.ok else {'error': r.text[:200]}

def trailing_stop(base, headers, symbol, qty, trail_pct=8.0):
    body = {'symbol':symbol,'qty':str(int(qty)),'side':'sell','type':'trailing_stop',
            'trail_percent':str(trail_pct),'time_in_force':'gtc'}
    r = requests.post(f'{base}/orders', headers=headers, data=json.dumps(body), timeout=12)
    return r.ok

def market_sell(base, headers, symbol, qty):
    body = {'symbol':symbol,'qty':str(int(qty)),'side':'sell','type':'market','time_in_force':'day'}
    r = requests.post(f'{base}/orders', headers=headers, data=json.dumps(body), timeout=12)
    return r.ok

def is_open(base, headers):
    try:
        r = requests.get(f'{base}/clock', headers=headers, timeout=10)
        return r.json().get('is_open', False)
    except: return False
