"""Simple API server for Monte Carlo simulations."""
import json, sys
sys.path.insert(0, 'src')
from mc.gbm import simulate, summary
from mc.cards import shuffle, deal
from mc.sports import poisson_match, elo_expected
from prob.bayes import BetaBernoulli
from prob.hypothesis import probabilistic_sharpe_ratio, deflated_sharpe_ratio

def handle(request):
    path = request.get('path', '')
    body = request.get('body', {})
    if path == '/api/mc/gbm':
        paths = simulate(body.get('spot', 100), body.get('mu', 0.1), body.get('sigma', 0.25),
                         body.get('horizon', 252), body.get('runs', 100000))
        return {'ok': True, 'data': summary(paths)}
    if path == '/api/mc/cards':
        n = body.get('n_hands', 2)
        return {'ok': True, 'data': deal(n, body.get('cards_per', 2))}
    if path == '/api/prob/bayes':
        bb = BetaBernoulli(body.get('alpha', 1), body.get('beta', 1))
        bb.update(body.get('successes', 0), body.get('failures', 0))
        return {'ok': True, 'data': {'mean': bb.posterior_mean(), 'ci': bb.credible_interval()}}
    if path == '/api/prob/psr':
        r = probabilistic_sharpe_ratio(body.get('returns', []))
        d = deflated_sharpe_ratio(body.get('returns', []), body.get('n_trials', 1))
        return {'ok': True, 'data': {'psr': r, 'dsr': d}}
    return {'ok': False, 'error': 'unknown path'}

if __name__ == '__main__':
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(n)) if n else {}
            res = handle({'path': self.path, 'body': body})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
    HTTPServer(('', 8080), H).serve_forever()
