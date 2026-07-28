"""Hypothesis testing — Probabilistic Sharpe Ratio, Deflated Sharpe Ratio."""
import numpy as np
from scipy import stats

def probabilistic_sharpe_ratio(returns, benchmark_sr=0.0, periods_per_year=252):
    r = np.asarray(returns, dtype=float)
    n = len(r)
    if n < 5 or r.std() == 0:
        return 0.0
    sr = r.mean() / r.std() * np.sqrt(periods_per_year)
    skew = stats.skew(r)
    kurt = stats.kurtosis(r, fisher=False)
    num = (sr - benchmark_sr) * np.sqrt(n - 1)
    den = np.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr**2)
    return float(stats.norm.cdf(num / den)) if den > 0 else 0.0

def deflated_sharpe_ratio(returns, n_trials, periods_per_year=252):
    r = np.asarray(returns, dtype=float)
    n = len(r)
    if n < 5 or r.std() == 0 or n_trials < 1:
        return 0.0
    sr = r.mean() / r.std()
    var_sr = (1/(n-1)) * (1 - stats.skew(r)*sr + (stats.kurtosis(r, fisher=False)-1)/4 * sr**2)
    sigma_sr = np.sqrt(max(var_sr, 1e-12))
    euler = 0.5772156649
    e_max = (1-euler)*stats.norm.ppf(1-1/n_trials) + euler*stats.norm.ppf(1-1/(n_trials*np.e))
    bench = sigma_sr * e_max
    num = (sr - bench) * np.sqrt(n - 1)
    skew = stats.skew(r)
    kurt = stats.kurtosis(r, fisher=False)
    den = np.sqrt(1 - skew*sr + (kurt-1)/4 * sr**2)
    return float(stats.norm.cdf(num/den)) if den > 0 else 0.0

def min_track_record(returns, target_sr=1.0, periods_per_year=252, conf=0.95):
    r = np.asarray(returns, dtype=float)
    if len(r) < 5 or r.std() == 0:
        return float('inf')
    sr = r.mean()/r.std()
    skew = stats.skew(r)
    kurt = stats.kurtosis(r, fisher=False)
    z = stats.norm.ppf(conf)
    target = target_sr/np.sqrt(periods_per_year)
    denom = (sr - target)**2
    return float('inf') if denom <= 0 else float(1 + (1 - skew*sr + (kurt-1)/4*sr**2) * (z/np.sqrt(denom))**2)
