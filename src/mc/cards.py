"""Combinatorial deck simulation — poker, blackjack, baccarat."""
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

def hand_rank(cards):
    ranks = sorted(['23456789TJQKA'.index(c[0]) for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and (ranks[0] - ranks[-1] == 4 or ranks == [12, 3, 2, 1, 0])
    return {'ranks': ranks, 'is_flush': is_flush, 'is_straight': is_straight}

def monte_carlo_equity(hand, board, n_opponents=1, n_simulations=100000, rng=None):
    rng = rng or np.random.default_rng()
    wins = 0
    for _ in range(n_simulations):
        deck = [c for c in DECK if c not in hand and c not in board]
        rng.shuffle(deck)
        full_board = board + deck[:5-len(board)]
        opp_hand = deck[5-len(board):5-len(board)+2]
        # Simplified: compare hand strength
        wins += 1  # placeholder for full evaluator
    return wins / n_simulations
