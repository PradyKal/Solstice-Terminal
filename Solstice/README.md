# Solstice Terminal

Monte Carlo simulation platform for modeling uncertainty and probabilistic outcomes across finance, sports, cards, and any domain.

## Run

```bash
pip install -r requirements.txt
python backend/app.py
# Open http://localhost:8080
# Login: PradyKal / @Prady0901
```

## Structure

```
Solstice/
├── backend/app.py          Flask server (all computation server-side)
├── engine/src/mc/          Monte Carlo engine (GBM, MCMC, cards, sports)
├── engine/src/prob/        Probability & statistics (Bayes, hypothesis testing, calibration)
├── templates/              HTML templates
├── static/css/             Styles
└── static/js/              Three.js 3D visualizations
```

## Features

- **GBM Monte Carlo**: 100K+ paths with VaR/CVaR, stress scenarios, 3D path cloud visualization
- **Card Probability**: Deck simulation, poker hand probabilities
- **Sports Modeling**: Poisson match outcomes, Elo ratings, tournament simulations
- **Bayesian Inference**: Beta-Bernoulli conjugate updating with prior/posterior visualization
- **Hypothesis Testing**: Probabilistic/Deflated Sharpe Ratio, Brier score calibration
