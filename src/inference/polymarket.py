"""Prediction market calibration and arbitrage detection."""
import numpy as np
from src.prob.bayes import BetaBernoulli

def calibrate(market_price, observed=None, prior_alpha=1, prior_beta=1):
    bb = BetaBernoulli(prior_alpha, prior_beta)
    if observed is not None:
        bb.update(observed, 1-observed)
    return {
        'market_price': market_price,
        'bayesian_price': bb.posterior_mean(),
        'credible_interval': bb.credible_interval(),
        'edge': bb.posterior_mean() - market_price,
    }

def arbitrage_opportunity(prices):
    """Detect arbitrage across mutually exclusive outcomes. Sum of prices > 1 = arb."""
    total = sum(prices)
    if total < 0.99:
        return {'arb': True, 'return': 1/total - 1, 'bet': [1/p/total for p in prices]}
    return {'arb': False, 'overround': total - 1}

def kelly_bet(probability, odds):
    b = odds - 1 if odds > 1 else 1/odds - 1
    q = 1 - probability
    f = (probability * b - q) / b
    return max(0, f) if b > 0 else 0
