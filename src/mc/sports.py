"""Sports probability models — Poisson, Elo, Bayesian skill."""
import numpy as np
from scipy import stats

def poisson_match(home_strength, away_strength, home_adv=0.15):
    lam_home = np.exp(home_strength + home_adv)
    lam_away = np.exp(away_strength)
    return {'home_win': 1 - stats.poisson.cdf(0, lam_home - lam_away) if lam_home > lam_away else 0.5}

def elo_expected(rating_a, rating_b):
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def elo_update(winner_rating, loser_rating, k=32):
    expected = elo_expected(winner_rating, loser_rating)
    return winner_rating + k * (1 - expected), loser_rating - k * (1 - expected)

def bayesian_skill(observed_wins, observed_losses, prior_alpha=2, prior_beta=2):
    posterior_alpha = prior_alpha + observed_wins
    posterior_beta = prior_beta + observed_losses
    return {
        'win_rate': posterior_alpha / (posterior_alpha + posterior_beta),
        'credible_interval': stats.beta.interval(0.95, posterior_alpha, posterior_beta)
    }
