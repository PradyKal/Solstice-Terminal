"""Parametric and non-parametric probability distributions."""
import numpy as np
from scipy import stats

def fit_normal(data):
    mu, sigma = stats.norm.fit(data)
    return {'mu': mu, 'sigma': sigma}

def fit_stable(data):
    alpha, beta, loc, scale = stats.levy_stable.fit(data)
    return {'alpha': alpha, 'beta': beta, 'loc': loc, 'scale': scale}

def kde_density(data, grid=100):
    kde = stats.gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), grid)
    return {'x': xs.tolist(), 'y': kde(xs).tolist()}

def mixture_density(components, weights):
    xs = np.linspace(-5, 5, 200)
    ys = np.zeros_like(xs)
    for (mu, sigma), w in zip(components, weights):
        ys += w * stats.norm.pdf(xs, mu, sigma)
    return {'x': xs.tolist(), 'y': (ys / ys.sum()).tolist()}
