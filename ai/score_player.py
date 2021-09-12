from ai.base import Recommender

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
    def strategy(self):
        return min(self._state.legal_choices, key=lambda x: self._score(x))

    @staticmethod
    def _score(state):
        alive = min(1, len(state.legal_choices))
        return sum(EXISTENCE_SCORE_TABLE[p.lower()] for p in state.pieces(state.next_side).values()) * alive / \
            sum(EXISTENCE_SCORE_TABLE[p.lower()] for p in state.pieces(state.next_side.OPPONENT).values())
