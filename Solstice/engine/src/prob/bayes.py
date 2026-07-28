"""Conjugate Bayesian updating — Beta-Bernoulli for binary outcomes."""
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

    def probability_greater_than(self, threshold):
        return 1 - stats.beta.cdf(threshold, self.alpha, self.beta)
