"""Sports probability."""
import numpy as np
from scipy import stats

def poisson_match(home_strength, away_strength, home_adv=0.15):
    lam_home = np.exp(home_strength + home_adv)
    lam_away = np.exp(away_strength)
    return {'home_win': 1 - stats.poisson.cdf(0, lam_home - lam_away) if lam_home > lam_away else 0.5}

def elo_expected(rating_a, rating_b):
    return 1 / (1 + 10**((rating_b - rating_a) / 400))
