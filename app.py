"""Solstice Terminal — Monte Carlo simulation platform.
All computation runs server-side in Python. Frontend is a thin display layer."""
import os, sys, json, hashlib, secrets
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from flask import Flask, render_template, request, jsonify, session, redirect
from mc.gbm import simulate, summary, stress_scenarios
from mc.cards import shuffle, deal, hand_probability
from mc.sports import poisson_match, elo_expected, simulate_tournament
from prob.bayes import BetaBernoulli
from prob.hypothesis import probabilistic_sharpe_ratio, deflated_sharpe_ratio
from prob.calibration import brier_score, reliability
import numpy as np

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

PASSWORD_HASH = hashlib.sha256(b'@Prady0901').hexdigest()
USERNAME = 'PradyKal'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    data = request.get_json() or {}
    u, p = data.get('username', ''), data.get('password', '')
    if u == USERNAME and hashlib.sha256(p.encode()).hexdigest() == PASSWORD_HASH:
        session['user'] = u
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'authentication failed'}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/terminal')
def terminal():
    if 'user' not in session:
        return redirect('/login')
    return render_template('terminal.html')

# ─── MC: GBM ───
@app.route('/api/mc/gbm', methods=['POST'])
def api_gbm():
    d = request.get_json() or {}
    spot = float(d.get('spot', 100))
    mu = float(d.get('mu', 0.10))
    sigma = float(d.get('sigma', 0.25))
    horizon = int(d.get('horizon', 252))
    runs = min(int(d.get('runs', 50000)), 200000)
    paths = simulate(spot, mu, sigma, horizon, runs)
    result = summary(paths)
    result['path_sample'] = paths[np.random.choice(runs, min(50, runs), replace=False)].round(4).tolist()
    return jsonify(result)

@app.route('/api/mc/stress', methods=['POST'])
def api_stress():
    d = request.get_json() or {}
    return jsonify(stress_scenarios(
        float(d.get('spot', 100)), float(d.get('mu', 0.10)), float(d.get('sigma', 0.25))
    ))

# ─── MC: Cards ───
@app.route('/api/mc/cards', methods=['POST'])
def api_cards():
    d = request.get_json() or {}
    hands = deal(int(d.get('n_hands', 2)), int(d.get('cards_per', 5)))
    return jsonify({'hands': hands})

@app.route('/api/mc/cards/probability', methods=['POST'])
def api_cards_prob():
    d = request.get_json() or {}
    prob = hand_probability(d.get('hand_type', 'pair'), min(int(d.get('n_simulations', 50000)), 200000))
    return jsonify({'hand_type': d.get('hand_type', 'pair'), 'probability': prob})

# ─── Sports ───
@app.route('/api/sports/poisson', methods=['POST'])
def api_poisson():
    d = request.get_json() or {}
    return jsonify(poisson_match(float(d.get('home_strength', 0.5)), float(d.get('away_strength', 0.2))))

@app.route('/api/sports/elo', methods=['POST'])
def api_elo():
    d = request.get_json() or {}
    return jsonify({'expected': elo_expected(float(d.get('rating_a', 1500)), float(d.get('rating_b', 1400)))})

@app.route('/api/sports/tournament', methods=['POST'])
def api_tournament():
    d = request.get_json() or {}
    return jsonify(simulate_tournament(d.get('ratings', [1500, 1400, 1300]), min(int(d.get('n_simulations', 10000)), 50000)))

# ─── Bayes ───
@app.route('/api/prob/bayes', methods=['POST'])
def api_bayes():
    d = request.get_json() or {}
    bb = BetaBernoulli(float(d.get('alpha', 1)), float(d.get('beta', 1)))
    bb.update(int(d.get('successes', 0)), int(d.get('failures', 0)))
    from scipy import stats
    xs = np.linspace(0.001, 0.999, 100)
    posterior = stats.beta.pdf(xs, bb.alpha, bb.beta).tolist()
    prior = stats.beta.pdf(xs, float(d.get('alpha', 1)), float(d.get('beta', 1))).tolist()
    return jsonify({
        'mean': bb.posterior_mean(), 'ci': list(bb.credible_interval()),
        'prob_gt_50': bb.probability_greater_than(0.5),
        'prior': prior, 'posterior': posterior, 'x': xs.tolist()
    })

# ─── Hypothesis ───
@app.route('/api/prob/hypothesis', methods=['POST'])
def api_hypothesis():
    d = request.get_json() or {}
    returns = d.get('returns', [])
    return jsonify({
        'psr': probabilistic_sharpe_ratio(returns),
        'dsr': deflated_sharpe_ratio(returns, int(d.get('n_trials', 1))),
        'brier': brier_score([0.5]*len(returns), [1 if r > 0 else 0 for r in returns]) if returns else 0
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
