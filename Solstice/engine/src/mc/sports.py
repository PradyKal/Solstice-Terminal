"""Sports probability models — Poisson match outcomes, Elo ratings, tournament simulations."""
import numpy as np
from scipy import stats

def poisson_match(home_strength=0.5, away_strength=0.2, home_adv=0.15):
    lam_home = np.exp(home_strength + home_adv)
    lam_away = np.exp(away_strength)
    prob_home = 1 - stats.poisson.cdf(0, lam_home - lam_away) if lam_home > lam_away else 0.5
    return {
        'home_win': prob_home,
        'draw': stats.poisson.pmf(0, abs(lam_home - lam_away)),
        'away_win': 1 - prob_home - stats.poisson.pmf(0, abs(lam_home - lam_away))
    }

def elo_expected(rating_a, rating_b):
    return 1 / (1 + 10**((rating_b - rating_a) / 400))

def elo_update(winner_rating, loser_rating, k=32):
    expected = elo_expected(winner_rating, loser_rating)
    return winner_rating + k * (1 - expected), loser_rating - k * (1 - expected)

def simulate_tournament(ratings, n_simulations=10000, rng=None):
    rng = rng or np.random.default_rng()
    n = len(ratings)
    wins = np.zeros(n)
    for _ in range(n_simulations):
        for i in range(n):
            for j in range(i+1, n):
                p = elo_expected(ratings[i], ratings[j])
                if rng.uniform() < p:
                    wins[i] += 1
                else:
                    wins[j] += 1
    total = wins.sum()
    return {f'player_{i}': float(wins[i]/total) for i in range(n)}
