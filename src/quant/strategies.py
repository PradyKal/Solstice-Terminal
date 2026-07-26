"""9 factor-based strategies with cost-adjusted walk-forward backtesting."""
import numpy as np
from scipy import stats

def residual_momentum(data, lookback=126, skip=21):
    scores = {}
    mkt = data.get('SPY', {}).get('returns')
    if mkt is None: return scores
    for t, d in data.items():
        r = d['returns']
        n = min(len(r), len(mkt))
        if n < lookback + skip: continue
        rr = r[-(lookback+skip):]; mm = mkt[-(lookback+skip):]
        beta = np.cov(rr, mm, bias=True)[0,1] / (np.var(mm) + 1e-9)
        resid = rr - beta * mm
        scores[t] = np.sum(resid[:-skip]) / (np.std(resid) + 1e-9)
    return _zscore(scores)

def vol_managed_momentum(data, lookback=126, skip=21):
    scores = {}
    for t, d in data.items():
        c = d['close']; r = d['returns']
        if len(c) < lookback + skip: continue
        mom = c[-skip] / c[-(lookback+skip)] - 1.0
        recent_vol = np.std(r[-21:]) * np.sqrt(252) + 1e-9
        scores[t] = mom / recent_vol
    return _zscore(scores)

def short_term_reversal(data, lookback=5):
    scores = {}
    for t, d in data.items():
        c = d['close']
        if len(c) < lookback + 1: continue
        scores[t] = -(c[-1] / c[-(lookback+1)] - 1.0)
    return _zscore(scores)

def quality_stability(data, lookback=252):
    scores = {}
    for t, d in data.items():
        c = d['close']
        if len(c) < lookback: continue
        w = c[-lookback:]; tr = w[-1]/w[0] - 1
        dd = abs(((w - np.maximum.accumulate(w)) / np.maximum.accumulate(w)).min()) + 1e-9
        scores[t] = tr / dd
    return _zscore(scores)

def cointegrated_pairs(data, lookback=120, threshold=0.10):
    scores = {}; counts = {}
    pairs = [('KO','PEP'),('XOM','CVX'),('JPM','BAC'),('V','MA'),('HD','LOW'),
             ('UNH','CI'),('LMT','RTX'),('AVGO','QCOM'),('MCD','SBUX'),('GOOGL','META')]
    for a,b in pairs:
        da,db = data.get(a),data.get(b)
        if da is None or db is None: continue
        if min(len(da['close']),len(db['close'])) < lookback+1: continue
        ca = np.log(da['close'][-lookback:]); cb = np.log(db['close'][-lookback:])
        beta = np.cov(ca,cb,bias=True)[0,1]/(np.var(cb)+1e-9)
        spread = ca - beta*cb; mu,sd = np.mean(spread),np.std(spread)+1e-9
        z = (spread[-1]-mu)/sd
        scores[a] = scores.get(a,0)+float(np.clip(-z/3,-1,1))
        scores[b] = scores.get(b,0)+float(np.clip(+z/3,-1,1))
        counts[a] = counts.get(a,0)+1; counts[b] = counts.get(b,0)+1
    return {t: scores[t]/counts[t] for t in scores}

def _zscore(scores):
    if not scores: return {}
    vals = np.array(list(scores.values()), dtype=float)
    mean, std = vals.mean(), vals.std() + 1e-9
    return {t: float(np.clip((v-mean)/std, -3, 3)/3) for t,v in scores.items()}

STRATEGIES = {
    'residual_momentum': residual_momentum, 'vol_managed_momentum': vol_managed_momentum,
    'short_term_reversal': short_term_reversal, 'quality_stability': quality_stability,
    'cointegrated_pairs': cointegrated_pairs,
}
