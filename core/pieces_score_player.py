from core.state import State

SCORE_TABLE = {
    'p': 2,
    'a': 3,
    'm': 3,
    'c': 5,
    'k': 5,
    'r': 10,
    'g': 1  # use a small value to ensure that the total result is positive
}  # 62 in total


class PiecesScorePlayer(State):
    depth = 4

    def strategy(self):
        return min(self.legal_choices, key=lambda x: x.score)

    @property
    def score(self):
        alive = min(1, len(self.legal_choices))
        return sum(SCORE_TABLE[self._occupation(p).lower()] for p in self.self_pieces) * alive / \
            sum(SCORE_TABLE[self._occupation(p).lower()] for p in self.oppo_pieces)


