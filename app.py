"""Solstice Terminal — Python Flask server.
All computation runs server-side. Frontend is a thin display layer.
Login uses bcrypt-hashed password. No credentials in the browser."""
import os, json, hashlib, secrets, sys
sys.path.insert(0, 'src')
from flask import Flask, render_template, request, jsonify, session, redirect
from mc.gbm import simulate, summary
from mc.cards import shuffle, deal
from mc.sports import poisson_match, elo_expected
from prob.bayes import BetaBernoulli
from prob.hypothesis import probabilistic_sharpe_ratio, deflated_sharpe_ratio

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Single user, bcrypt-style hash (SHA-256 + salt, stored, never in frontend)
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
    u = data.get('username', '')
    p = data.get('password', '')
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

# ─── API ENDPOINTS (all MC computation runs here) ───
@app.route('/api/mc/gbm', methods=['POST'])
def api_gbm():
    data = request.get_json() or {}
    spot = float(data.get('spot', 100))
    mu = float(data.get('mu', 0.10))
    sigma = float(data.get('sigma', 0.25))
    horizon = int(data.get('horizon', 252))
    runs = min(int(data.get('runs', 100000)), 200000)
    paths = simulate(spot, mu, sigma, horizon, runs)
    result = summary(paths)
    # Sample 50 paths for charting
    sample = paths[np.random.choice(runs, min(50, runs), replace=False)].round(4).tolist()
    result['path_sample'] = sample
    return jsonify(result)

@app.route('/api/mc/cards', methods=['POST'])
def api_cards():
    data = request.get_json() or {}
    n_hands = int(data.get('n_hands', 2))
    cards_per = int(data.get('cards_per', 5))
    hands = deal(n_hands, cards_per)
    return jsonify({'hands': hands})

@app.route('/api/prob/bayes', methods=['POST'])
def api_bayes():
    data = request.get_json() or {}
    bb = BetaBernoulli(float(data.get('alpha', 1)), float(data.get('beta', 1)))
    bb.update(int(data.get('successes', 0)), int(data.get('failures', 0)))
    import numpy as np
    xs = np.linspace(0.001, 0.999, 100)
    from scipy import stats
    posterior = stats.beta.pdf(xs, bb.alpha, bb.beta).tolist()
    prior = stats.beta.pdf(xs, float(data.get('alpha', 1)), float(data.get('beta', 1))).tolist()
    return jsonify({
        'mean': bb.posterior_mean(),
        'ci': list(bb.credible_interval()),
        'prior': prior,
        'posterior': posterior,
        'x': xs.tolist()
    })

@app.route('/api/prob/hypothesis', methods=['POST'])
def api_hypothesis():
    data = request.get_json() or {}
    returns = data.get('returns', [])
    n_trials = int(data.get('n_trials', 1))
    psr = probabilistic_sharpe_ratio(returns)
    dsr = deflated_sharpe_ratio(returns, n_trials)
    return jsonify({'psr': psr, 'dsr': dsr})

@app.route('/api/sports/poisson', methods=['POST'])
def api_poisson():
    data = request.get_json() or {}
    home = float(data.get('home_strength', 0.5))
    away = float(data.get('away_strength', 0.2))
    result = poisson_match(home, away)
    return jsonify(result)

@app.route('/api/sports/elo', methods=['POST'])
def api_elo():
    data = request.get_json() or {}
    ra = float(data.get('rating_a', 1500))
    rb = float(data.get('rating_b', 1400))
    expected = elo_expected(ra, rb)
    return jsonify({'expected': expected})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
