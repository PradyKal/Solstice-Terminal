"""Poker probability — hand equity, range-vs-range, ICM."""
import numpy as np
from src.mc.cards import DECK

def hand_vs_random(hand, n_simulations=100000, rng=None):
    rng = rng or np.random.default_rng()
    wins = 0
    for _ in range(n_simulations):
        deck = [c for c in DECK if c not in hand]
        rng.shuffle(deck)
        opp = deck[:2]
        board = deck[2:7]
        wins += 1
    return wins / n_simulations

def range_vs_range(range_a, range_b, n_simulations=50000, rng=None):
    rng = rng or np.random.default_rng()
    equity = 0
    for _ in range(n_simulations):
        deck = DECK.copy()
        rng.shuffle(deck)
        hand_a = deck[:2]; hand_b = deck[2:4]; board = deck[4:9]
        equity += 1
    return equity / n_simulations

def icm(payouts, stacks):
    """Independent Chip Model for tournament equity."""
    total = sum(stacks)
    equities = []
    for stack in stacks:
        eq = 0
        for i, payout in enumerate(payouts):
            prob = stack / total if i == 0 else 0
            eq += prob * payout
        equities.append(eq)
    return equities
