# Solstice Terminal Pradyun Kalagara

Monte Carlo simulation platform for modeling uncertainty and probabilistic outcomes across any domain.

Main methods: Bayesian inference, MCMC sampling, and hypothesis testing with 3D model visualization built with Physics & entropy. 

24 Research Papers cited across physics, mathematics, finance, economics, statistics, game theory, weather forecasting & other probability modeling fields. 
14 total models built from past research applied to financial mathematics

## Structure

```
solstice-terminal/
├── README.md
├── requirements.txt
├── backend/
│   └── app.py              # Flask server (all computation server-side)
├── frontend/
│   ├── index.html           # Landing page
│   ├── login.html           # Login form (posts to server, SHA-256 hashed)
│   └── terminal.html        # Terminal UI (calls API endpoints, no local computation)
├── engine/
│   └── src/
│       ├── mc/              # Monte Carlo engine
│       │   ├── gbm.py       # Geometric Brownian Motion (stock/crypto simulation)
│       │   ├── sampler.py   # MCMC, importance sampling
│       │   ├── cards.py     # Deck simulation, poker probabilities
│       │   └── sports.py    # Poisson match outcomes, Elo ratings
│       └── prob/            # Probability & statistics
│           ├── bayes.py     # Beta-Bernoulli conjugate Bayesian updating
│           ├── hypothesis.py # Probabilistic/Deflated Sharpe Ratio
│           ├── calibration.py # Brier score, reliability diagrams
│           └── distributions.py # Normal fitting, KDE, mixture models
└── templates/               # HTML templates for Flask
    ├── index.html
    ├── login.html
    └── terminal.html
```

```
```

## What it does

- **SIMULATE**: Run 100K+ Monte Carlo paths on any asset with VaR/CVaR
- **STRESS TEST**: Vol shocks, bear markets, crash scenarios
- **CARDS**: Poker hand probabilities, deck simulation
- **SPORTS**: Poisson match outcomes, Elo ratings, tournament sims
- **Finance**: Financial modeling, equity probability movement, monthly updates using up to date research in the field
- **BAYES**: Update old conclusions with new evidence
- **HYPOTHESIS TEST**: Probabilistic/Deflated Sharpe Ratio

All computation runs in Python. The browser is just a display layer.
