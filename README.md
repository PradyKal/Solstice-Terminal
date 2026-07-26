# Solstice Terminal

Monte Carlo simulation platform for modeling uncertainty and probabilistic outcomes.

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
src/prob/           Probability & statistics (distributions, Bayesian, hypothesis testing)
```

All computation runs in Python on the server. The browser is a thin display layer.
