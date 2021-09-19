from ai.base import Recommender
from cache import cache

EXISTENCE_SCORE_TABLE = {
    'p': 2,
    'a': 3,
    'm': 3,
    'c': 5,
    'k': 5,
    'r': 10,
    'g': 1  # use a small value to ensure that the total result is positive
}  # 62 in total


class ScoreRecommender(Recommender):
    def __init__(self, power=2):
        self._power_argument = power
        self._cache = {}

    def strategy(self, state):
        return min(cache.legal_movements(state), key=lambda x: self.score(x))

    def score(self, state):
        if state not in self._cache:
            self._cache[state] = self._score(state)
        return self._cache[state]

    def _score(self, state):
        # Power score is the sum of total strength of a side.
        # It quantifies the absolute power in long term.
        self_power = sum(EXISTENCE_SCORE_TABLE[p.lower()] for p in state.pieces(state.next_side).values())
        oppo_power = sum(EXISTENCE_SCORE_TABLE[p.lower()] for p in state.pieces(state.next_side.OPPONENT).values())
        # Agile score is the total number of controlling points of one side.
        # It quantifies the flexibility of the pieces for a specific layout.
        self_agile = len(state.valid_choices(state.next_side))
        oppo_agile = len(state.valid_choices(state.next_side.OPPONENT))
        # Alive score is a binary number indicating whether self is alive or not.
        # It will only resulted in 0 if no legal choice found,
        # which means that the next player has already lost the game.
        # This score is necessary for the final phase.
        alive_score = min(1, len(cache.legal_movements(state)))

        return alive_score * (self_agile + self_power * self._power_argument) / (oppo_agile + oppo_power * self._power_argument)
