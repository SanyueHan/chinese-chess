

DEFAULT_SCORE_TABLE = {
    'p': 2,
    'a': 3,
    'm': 3,
    'c': 5,
    'k': 5,
    'r': 10,
    'g': 1  # use a small value to ensure that the total result is positive
}  # 62 in total


class ScoreCalculator:
    def __init__(self, score_table=None):
        self._score_table = score_table if score_table else DEFAULT_SCORE_TABLE
        self._score_cache = {}

    def score(self, state):
        if state not in self._score_cache:
            self._score_cache[state] = self._score(state)
        return self._score_cache[state]

    def _score(self, state):
        self_power = sum(self._score_table[p.lower()] for p in state.pieces(state.next_side).values())
        oppo_power = sum(self._score_table[p.lower()] for p in state.pieces(state.next_side.opponent).values())
        alive_score = 1 if state.general_position(state.next_side) else 0

        return alive_score * self_power / oppo_power
