# Solstice Terminal

**Universal Monte Carlo Probability Engine**

A mathematically rigorous simulation framework for probabilistic inference across any domain — financial markets, poker, sports betting, card games, election forecasting, or any system with measurable uncertainty.

Built on Bayesian Monte Carlo methods with path-integral sampling, conjugate prior updating, and deflated-Sharpe hypothesis testing.

---

## Core Architecture

```
src/
├── mc/                  # Monte Carlo engine
│   ├── sampler.py       # MCMC, importance sampling, SMC
│   ├── gbm.py           # Geometric Brownian Motion (finance)
│   ├── cards.py         # Deck simulation, combinatorial enumeration
│   └── sports.py        # Poisson / Elo / Bayesian skill models
│
├── prob/                # Probability & statistics
│   ├── distributions.py # Parametric + non-parametric densities
│   ├── bayes.py         # Conjugate priors, Bayesian updating
│   ├── hypothesis.py    # Deflated Sharpe, PSR, multiple-testing
│   └── calibration.py   # Probability calibration (Brier, log-loss)
│
├── inference/           # Applied inference
│   ├── polymarket.py    # Prediction market arbitrage detection
│   ├── poker.py         # Hand equity, range vs range, ICM
│   └── finance.py       # Factor models, Kelly criterion, vol targeting
│
└── quant/               # Live quant trading engine (Alpaca)
    ├── strategies.py    # 9 factor-based strategies
    ├── risk.py          # Sector caps, drawdown breaker, trailing stops
    ├── execution.py     # Alpaca bracket orders
    └── runner.py        # Weekly automated pipeline
```

## Mathematical Foundation

### Monte Carlo Sampling
- **Path-integral GBM**: `S_t = S_0 · exp((μ − σ²/2)t + σW_t)` with antithetic variates for variance reduction
- **Sequential Monte Carlo**: Adaptive resampling for non-linear state spaces
- **MCMC (Metropolis-Hastings)**: Posterior sampling for Bayesian calibration

### Hypothesis Testing (Bailey & López de Prado, 2014)
- **Probabilistic Sharpe Ratio**: `PSR = Φ[(SR − SR_bench)√(n−1) / √(1 − γ·SR + (κ−1)/4 · SR²)]`
- **Deflated Sharpe Ratio**: Corrects for multiple-testing selection bias across N trials
- **Minimum Track Record Length**: Periods needed before a Sharpe is statistically significant

### Bayesian Updating
- Conjugate prior families for rapid online learning
- Beta-Bernoulli for win rates, Normal-Inverse-Gamma for return distributions
- Sequential posterior updating as new observations arrive

### Kelly Criterion
- `f* = (p·b − q) / b` for binary outcomes
- `f* = μ / σ²` for continuous (half-Kelly for safety)
- Multi-asset Kelly with covariance penalty

---

## Domains

| Domain | Model | Example |
|--------|-------|---------|
| **Finance** | GBM + factor models | 9-strategy quant engine, live Alpaca trading |
| **Prediction Markets** | Bayesian calibration + arbitrage | Detect mispriced contracts on Polymarket |
| **Poker** | Range equity + ICM | Hand-vs-range Monte Carlo, tournament ICM |
| **Sports** | Poisson / Elo / Bayesian skill | Score-line probabilities, spread covering |
| **Cards** | Combinatorial enumeration | Blackjack, baccarat, any finite-deck game |
| **Elections** | Poll aggregation + Bayesian | Forecast probabilities with uncertainty intervals |

---

## Quant Engine (Live)

The system runs a **weekly autonomous trading cycle** on Alpaca paper:

1. **9 strategies** backtested cost-adjusted with walk-forward validation
2. **Deflated Sharpe** gating — only strategies that survive multiple-testing correction deploy
3. **Kelly-sized** position allocation across strategy sleeves
4. **Sector caps** (SEMI 25%, others 30%), drawdown circuit breaker, 15% vol target
5. **Bracket orders** with trailing stops (5-8%, profit-tightened)
6. **News sentiment** screen with bad-news veto

Current live P&L: **+5.9%** since inception, max drawdown −0.3%, Sharpe 7.65 (30d window).

---

## Quick Start

```bash
git clone https://github.com/PradyKal/Solstice-Terminal
cd Solstice-Terminal

# Universal MC simulation
python -c "from src.mc.gbm import simulate; paths = simulate(spot=100, mu=0.10, sigma=0.25, horizon=252, runs=100000)"

# Poker hand equity
python -c "from src.inference.poker import hand_vs_range; equity = hand_vs_range('AhKh', 'AA,KK,AKs')"

# Prediction market calibration
python -c "from src.inference.polymarket import calibrate; cal = calibrate(observed=0.65, market_price=0.55)"
```

## Dependencies

`numpy`, `scipy`, `pandas`, `yfinance`, `requests`, `textblob`, `statsmodels`

---

*"All models are wrong, but some are useful." — George Box*
