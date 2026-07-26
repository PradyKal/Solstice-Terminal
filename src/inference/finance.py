"""Financial probability — Kelly criterion, factor models, volatility targeting."""
import numpy as np

def kelly_fraction(win_prob, win_loss_ratio):
    b = win_loss_ratio; p = win_prob; q = 1-p
    return max(0, (p*b - q) / b) if b > 0 else 0

def half_kelly(win_prob, win_loss_ratio):
    return kelly_fraction(win_prob, win_loss_ratio) * 0.5

def continuous_kelly(expected_return, variance, max_frac=0.05, multiplier=0.5):
    if variance <= 0 or expected_return <= 0: return 0.0
    return min(max_frac, max(0, expected_return / variance * multiplier))

def volatility_target(portfolio_vol, target_vol=0.15):
    return min(1.5, max(0.4, target_vol / (portfolio_vol + 1e-9)))

def factor_model(returns, factor_returns):
    X = np.column_stack([np.ones(len(factor_returns)), factor_returns])
    beta = np.linalg.lstsq(X, returns, rcond=None)[0]
    return {'alpha': beta[0], 'betas': beta[1:].tolist(), 'residual_vol': float(np.std(returns - X @ beta))}
