"""Probability calibration."""
import numpy as np

def reliability(probabilities, outcomes, n_bins=10):
    probs = np.array(probabilities); outcomes = np.array(outcomes)
    bins = np.linspace(0, 1, n_bins+1)
    bin_means, bin_accs = np.zeros(n_bins), np.zeros(n_bins)
    for i in range(n_bins):
        mask = (probs >= bins[i]) & (probs < bins[i+1])
        if mask.sum() > 0:
            bin_means[i] = probs[mask].mean()
            bin_accs[i] = outcomes[mask].mean()
    return {'bin_centers': ((bins[:-1]+bins[1:])/2).tolist(), 'bin_means': bin_means.tolist(), 'bin_accs': bin_accs.tolist()}

def expected_calibration_error(probabilities, outcomes, n_bins=10):
    probs = np.array(probabilities); outcomes = np.array(outcomes)
    bins = np.linspace(0, 1, n_bins+1); ece = 0.0
    for i in range(n_bins):
        mask = (probs >= bins[i]) & (probs < bins[i+1])
        if mask.sum() > 0:
            ece += abs(probs[mask].mean() - outcomes[mask].mean()) * mask.sum()
    return float(ece / len(probs))
