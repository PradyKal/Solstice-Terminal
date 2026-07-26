# Solstice Terminal

Monte Carlo simulation platform for modeling uncertainty and probabilistic outcomes across any domain.

## Structure

```
src/mc/          Monte Carlo engine (GBM, MCMC, cards, sports)
src/prob/        Probability & statistics (distributions, Bayesian, hypothesis testing, calibration)
server.py        API server
index.html       Landing page
login.html       Login (PradyKal / @Prady0901)
terminal.html    Terminal with Monte Carlo simulator, card probability, sports models, Bayesian inference
```

## Quick Start

```bash
python -c "from src.mc.gbm import simulate; paths = simulate(spot=100, mu=0.10, sigma=0.25, horizon=252, runs=100000)"
```

Open `index.html` in a browser to use the terminal interface.
