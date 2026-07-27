"""MCMC, importance sampling, Sequential Monte Carlo."""
import numpy as np

def metropolis_hastings(log_target, n_samples=5000, proposal_std=0.1, init=0.0, burn=1000, rng=None):
    rng = rng or np.random.default_rng()
    chain = [init]
    for _ in range(n_samples + burn - 1):
        prop = chain[-1] + rng.normal(0, proposal_std)
        log_accept = log_target(prop) - log_target(chain[-1])
        if np.log(rng.uniform()) < log_accept:
            chain.append(prop)
        else:
            chain.append(chain[-1])
    return np.array(chain[burn:])

def importance_sampling(log_weight, n_samples=10000, proposal_fn=None, rng=None):
    rng = rng or np.random.default_rng()
    proposal_fn = proposal_fn or (lambda r: r.normal(0, 1))
    samples = np.array([proposal_fn(rng) for _ in range(n_samples)])
    weights = np.exp(np.array([log_weight(s) for s in samples]))
    weights /= weights.sum()
    return samples, weights
