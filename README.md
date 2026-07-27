# Solstice Terminal

Monte Carlo simulation platform for modeling uncertainty and probabilistic outcomes across any domain.

## Run

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:8080
```

Login: `PradyKal` / `@Prady0901`

## Structure

```
app.py              Flask server (all computation server-side)
templates/          HTML templates (no logic, no credentials)
src/mc/             Monte Carlo engine (GBM, MCMC, cards, sports)
src/prob/           Probability & statistics (Bayesian, hypothesis testing, calibration)
```

## What you can do

- **SIMULATE**: Run 100K+ Monte Carlo paths on any asset (stock, crypto, etc.) with VaR/CVaR/probability distributions
- **STRESS TEST**: See how assets perform under vol shocks, bear markets, or crash scenarios
- **CARDS**: Simulate poker hands, calculate flush/straight/pair probabilities
- **SPORTS**: Poisson match outcomes, Elo ratings, tournament simulations
- **BAYES**: Update beliefs with new evidence — Beta-Bernoulli conjugate priors
- **HYPOTHESIS TEST**: Probabilistic/Deflated Sharpe Ratio — is your strategy real or luck?

All computation runs in Python. The browser is just a display layer.
