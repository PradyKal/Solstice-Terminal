"""Probability distributions."""
import numpy as np
from scipy import stats

def fit_normal(data):
    mu, sigma = stats.norm.fit(data)
    return {'mu': mu, 'sigma': sigma}

def kde_density(data, grid=100):
    kde = stats.gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), grid)
    return {'x': xs.tolist(), 'y': kde(xs).tolist()}
