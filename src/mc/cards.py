"""Deck simulation and combinatorial enumeration."""
import numpy as np
from itertools import combinations

RANKS = '23456789TJQKA'
SUITS = 'cdhs'
DECK = [r+s for r in RANKS for s in SUITS]

def shuffle(rng=None):
    rng = rng or np.random.default_rng()
    return rng.permutation(DECK).tolist()

def deal(n_hands=2, cards_per=2, rng=None):
    deck = shuffle(rng)
    return [deck[i::n_hands][:cards_per] for i in range(n_hands)]

def enumerate_combos(deck, n=5):
    return list(combinations(deck, n))
