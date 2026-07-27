"""Deck simulation for poker, blackjack, any card game probability."""
import numpy as np
from itertools import combinations

RANKS = '23456789TJQKA'
SUITS = ['♠', '♥', '♦', '♣']
DECK = [r+s for r in RANKS for s in SUITS]

def shuffle(rng=None):
    rng = rng or np.random.default_rng()
    return rng.permutation(DECK).tolist()

def deal(n_hands=2, cards_per=5, rng=None):
    deck = shuffle(rng)
    return [deck[i::n_hands][:cards_per] for i in range(n_hands)]

def hand_probability(hand_type='pair', n_simulations=100000, rng=None):
    """Monte Carlo estimate of being dealt a specific hand type."""
    rng = rng or np.random.default_rng()
    count = 0
    for _ in range(n_simulations):
        deck = rng.permutation(DECK).tolist()
        hand = deck[:5]
        ranks = sorted([c[0] for c in hand])
        if hand_type == 'pair':
            if len(set(ranks)) <= 4:
                count += 1
        elif hand_type == 'flush':
            if len(set(c[1] for c in hand)) == 1:
                count += 1
        elif hand_type == 'straight':
            vals = sorted('23456789TJQKA'.index(c[0]) for c in hand)
            if vals[-1] - vals[0] == 4 and len(set(vals)) == 5:
                count += 1
    return count / n_simulations
