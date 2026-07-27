"""Geometric Brownian Motion Monte Carlo — models stock prices, crypto, any asset with drift + volatility."""
import numpy as np

def simulate(spot, mu, sigma, horizon=252, runs=100000, antithetic=True, rng=None):
    rng = rng or np.random.default_rng()
    dt = 1.0 / 252  # daily timestep
    drift = (mu - 0.5 * sigma**2) * dt
    vol = sigma * np.sqrt(dt)
    if antithetic:
        n = runs // 2
        z = rng.normal(0, 1, (n, horizon))
        z = np.concatenate([z, -z], axis=0)
    else:
        z = rng.normal(0, 1, (runs, horizon))
    paths = spot * np.exp(np.cumsum(drift + vol * z, axis=1))
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
        'percentiles': {f'p{p}': float(np.percentile(ret, p)) for p in [1, 5, 25, 50, 75, 95, 99]}
    }

def stress_scenarios(spot, mu, sigma, horizon=252, runs=50000):
    return {
        'base': summary(simulate(spot, mu, sigma, horizon, runs)),
        'vol_2x': summary(simulate(spot, mu, sigma*2, horizon, runs)),
        'bear': summary(simulate(spot, mu-0.01, sigma*1.5, horizon, runs)),
        'crash': summary(simulate(spot, -0.03, sigma*2.5, horizon, runs)),
    }
