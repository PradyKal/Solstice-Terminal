"""Conjugate Bayesian updating — Beta-Bernoulli, Normal-Inverse-Gamma."""
import numpy as np
from scipy import stats

class BetaBernoulli:
    def __init__(self, alpha=1, beta=1):
        self.alpha, self.beta = alpha, beta
    def update(self, successes, failures):
        self.alpha += successes
        self.beta += failures
    def posterior_mean(self):
        return self.alpha / (self.alpha + self.beta)
    def credible_interval(self, prob=0.95):
        return stats.beta.interval(prob, self.alpha, self.beta)
    def sample(self, n=1000, rng=None):
        rng = rng or np.random.default_rng()
        return rng.beta(self.alpha, self.beta, n)

class NormalInverseGamma:
    def __init__(self, mu_0=0, kappa_0=1, alpha_0=1, beta_0=1):
        self.mu_0, self.kappa_0 = mu_0, kappa_0
        self.alpha_0, self.beta_0 = alpha_0, beta_0
    def update(self, data):
        n = len(data)
        x_bar = np.mean(data)
        self.mu_0 = (self.kappa_0 * self.mu_0 + n * x_bar) / (self.kappa_0 + n)
        self.kappa_0 += n
        self.alpha_0 += n / 2
        self.beta_0 += 0.5 * np.sum((data - x_bar)**2) + (self.kappa_0 * n * (x_bar - self.mu_0)**2) / (2 * (self.kappa_0 + n))
    def posterior_mean(self):
        return self.mu_0
    def posterior_var(self):
        return self.beta_0 / (self.alpha_0 - 1) * (1 + 1/self.kappa_0)
