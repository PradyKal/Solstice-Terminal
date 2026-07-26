"""MCMC, Sequential Monte Carlo, Importance Sampling."""
import numpy as np

def metropolis_hastings(log_target, n_samples, proposal_std=0.1, init=0.0, rng=None):
    rng = rng or np.random.default_rng()
    chain = [init]
    for _ in range(n_samples - 1):
        prop = chain[-1] + rng.normal(0, proposal_std)
        log_accept = log_target(prop) - log_target(chain[-1])
        if np.log(rng.uniform()) < log_accept:
            chain.append(prop)
        else:
            chain.append(chain[-1])
    return np.array(chain)

def importance_sampling(log_weight, n_samples, proposal_fn, rng=None):
    rng = rng or np.random.default_rng()
    samples = np.array([proposal_fn(rng) for _ in range(n_samples)])
    weights = np.exp(np.array([log_weight(s) for s in samples]))
    weights /= weights.sum()
    return samples, weights

def sequential_monte_carlo(transition_fn, observation_fn, n_particles, steps, rng=None):
    rng = rng or np.random.default_rng()
    particles = rng.normal(0, 1, n_particles)
    for t in range(steps):
        particles = transition_fn(particles, t, rng)
        weights = observation_fn(particles, t)
        weights = np.exp(weights - weights.max())
        weights /= weights.sum()
        if 1 / (weights**2).sum() < n_particles / 2:
            idx = rng.choice(n_particles, n_particles, p=weights)
            particles = particles[idx]
    return particles
