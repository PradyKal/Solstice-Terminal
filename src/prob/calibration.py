"""Probability calibration — reliability diagrams, Platt scaling, isotonic regression."""
import numpy as np
from scipy import stats

def reliability(probabilities, outcomes, n_bins=10):
    probs = np.array(probabilities); outcomes = np.array(outcomes)
    bins = np.linspace(0, 1, n_bins+1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_means = np.zeros(n_bins); bin_accs = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (probs >= bins[i]) & (probs < bins[i+1])
        if mask.sum() > 0:
            bin_means[i] = probs[mask].mean()
            bin_accs[i] = outcomes[mask].mean()
    return {'bin_centers': bin_centers.tolist(), 'bin_means': bin_means.tolist(), 'bin_accs': bin_accs.tolist()}

def expected_calibration_error(probabilities, outcomes, n_bins=10):
    props = np.array(probabilities); outcomes = np.array(outcomes)
    bins = np.linspace(0, 1, n_bins+1); ece = 0.0
    for i in range(n_bins):
        mask = (props >= bins[i]) & (props < bins[i+1])
        if mask.sum() > 0:
            ece += abs(props[mask].mean() - outcomes[mask].mean()) * mask.sum()
    return float(ece / len(props))
