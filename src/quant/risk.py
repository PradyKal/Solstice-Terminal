"""Risk management — sector caps, drawdown breaker, trailing stops."""
import numpy as np

SECTORS = {
    'SEMI': ['NVDA','AMD','MU','LRCX','KLAC','AMAT','QCOM','INTC','ADI','AVGO','TXN','SMH','SOXX'],
    'TECH': ['AAPL','MSFT','ORCL','CSCO','ADBE','CRM','INTU','PANW','ANET','ACN','NOW','IBM'],
    'FIN':  ['JPM','BAC','WFC','GS','MS','BLK','SPGI','SCHW','C','AXP','PGR','CB','MMC','ICE','BX'],
    'ENERGY':['XOM','CVX','COP','EOG','SLB','PSX','MPC','OXY'],
    'HEALTH':['LLY','JNJ','UNH','ABBV','MRK','TMO','PFE','ABT','AMGN','DHR','GILD','ISRG','VRTX','SYK','BSX','MDT','REGN','ELV','CI'],
    'CONS':  ['AMZN','TSLA','HD','MCD','NKE','LOW','SBUX','TJX','BKNG','WMT','PG','COST','KO','PEP','PM'],
    'IND':   ['CAT','UNP','GE','HON','BA','RTX','LMT','DE','ETN','TT','WM'],
    'COMM':  ['META','GOOGL','GOOG','DIS','NFLX','TMUS','VZ','T'],
    'OTHER': ['LIN','NEE','PLD','SPY','QQQ','IWM','XLU','XLB','XLRE','XLC','XLK','XLF','XLE','XLV','XLY','XLP','XLI'],
}

def sector_of(ticker):
    for sec, names in SECTORS.items():
        if ticker in names: return sec
    return 'OTHER'

class RiskManager:
    def __init__(self, equity):
        self.equity = float(equity)
        self.peak = float(equity)
        self.caps = {'SEMI': 0.25, 'OTHER': 0.30}
    def _cap(self, sec): return self.caps.get(sec, 0.30)
    def drawdown(self): return (self.equity - self.peak) / self.peak if self.peak > 0 else 0.0
    def exposure_mult(self):
        dd = abs(min(0, self.drawdown()))
        for level, m in [(0.05, 0.7), (0.10, 0.4), (0.15, 0.0)]:
            if dd >= level: return m
        return 1.0
    def vol_scalar(self, port_vol, target=0.15):
        return float(np.clip(target / (port_vol*np.sqrt(252) + 1e-9), 0.4, 1.5))
    def sector_exposure(self, positions):
        total = sum(abs(float(p.get('market_value',0))) for p in positions) or 1.0
        exp = {}
        for p in positions:
            sec = sector_of(p.get('symbol',p.get('ticker')))
            exp[sec] = exp.get(sec,0) + abs(float(p.get('market_value',0)))/total
        return exp
    def overweights(self, positions):
        total = sum(abs(float(p.get('market_value',0))) for p in positions) or 1.0
        by_sec = {}
        for p in positions:
            sec = sector_of(p.get('symbol')); by_sec.setdefault(sec,[]).append(p)
        trims = {}
        for sec, ps in by_sec.items():
            cap = self._cap(sec)*total; sec_d = sum(abs(float(p['market_value'])) for p in ps)
            excess = sec_d - cap
            if excess <= 0: continue
            for p in sorted(ps, key=lambda x:-abs(float(x['market_value']))):
                if excess <= 0: break
                cut = min(abs(float(p['market_value'])), excess)
                trims[p['symbol']] = cut; excess -= cut
        return trims
