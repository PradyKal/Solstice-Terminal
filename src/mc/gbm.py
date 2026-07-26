"""Geometric Brownian Motion Monte Carlo."""
import numpy as np

def simulate(spot, mu, sigma, horizon=252, runs=100000, rng=None):
    rng = rng or np.random.default_rng()
    dt = 1.0
    drift = (mu - 0.5 * sigma**2) * dt
    z = rng.normal(0, 1, (runs, horizon))
    paths = spot * np.exp(np.cumsum(drift + sigma * np.sqrt(dt) * z, axis=1))
    return paths

def summary(paths):
    finals = paths[:, -1]
    ret = finals / paths[:, 0] - 1
    return {
        'mean_return': float(ret.mean()),
        'median_return': float(np.median(ret)),
        'std_return': float(ret.std()),
        'var_95': float(np.percentile(ret, 5)),
        'cvar_95': float(ret[ret <= np.percentile(ret, 5)].mean()),
        'prob_up': float((ret > 0).mean()),
        'percentiles': {f'p{p}': float(np.percentile(ret, p)) for p in [1,5,25,50,75,95,99]}
    }
