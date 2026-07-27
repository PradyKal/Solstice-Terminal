"""Probability distributions — fitting, KDE, mixture models."""
import numpy as np
from scipy import stats

def fit_normal(data):
    mu, sigma = stats.norm.fit(data)
    return {'mu': mu, 'sigma': sigma}

def kde_density(data, grid=100):
    kde = stats.gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), grid)
    return {'x': xs.tolist(), 'y': kde(xs).tolist()}

def mixture_density(components, weights, grid=200):
    """components: [(mu, sigma), ...], weights: [w1, w2, ...]"""
    xs = np.linspace(-4, 4, grid)
    ys = np.zeros_like(xs)
    for (mu, sigma), w in zip(components, weights):
        ys += w * stats.norm.pdf(xs, mu, sigma)
    return {'x': xs.tolist(), 'y': (ys/ys.sum()).tolist()}
