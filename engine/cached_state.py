from engine.evaluable_state import EvaluableState


class CachedState(EvaluableState):
    """
    Using a global instance cache to avoid the same situation calculated multiple time
    """

    CACHE = {}
    HIT = 0
    MISS = 0

    @property
    def feature(self):
        return f"{self._board}{self._current_player}"

    @classmethod
    def from_board_and_role(cls, board, role):
        new = cls(board, role)
        if new.feature in cls.CACHE:
            cls.HIT += 1
            return cls.CACHE[new.feature]
        else:
            cls.MISS += 1
            cls.CACHE[new.feature] = new
            return new
