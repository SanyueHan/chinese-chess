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
        return f"{self._board}{self._next_side}"

    @classmethod
    def create_with_cache(cls, board, next_side):
        new = cls(board, next_side)
        if new.feature in cls.CACHE:
            cls.HIT += 1
            return cls.CACHE[new.feature]
        else:
            cls.CACHE[new.feature] = new
            cls.MISS += 1
            return new

    def create_from_vector(self, vector):
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        board = [list(line) for line in self]
        board[i_f][j_f] = board[i_s][j_s]
        board[i_s][j_s] = " "
        return self.create_with_cache(tuple(''.join(line) for line in board), self._next_side.opponent)
