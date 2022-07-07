from typing import Tuple, List

from constants import Role, SIDE
from core import StateBase
from core.errors import RuleViolatedError
from core.rules.pieces import *
from core.rules.targets import TARGETS


DEFAULT_SCORE_TABLE = {
    'p': 2,
    'a': 3,
    'm': 3,
    'c': 5,
    'k': 5,
    'r': 10,
    'g': 1  # use a small value to ensure that the total result is positive
}  # 62 in total


class StateForMachine(StateBase):
    SCORE_TABLE = {
        'p': 2,
        'a': 3,
        'm': 3,
        'c': 5,
        'k': 5,
        'r': 10,
        'g': 1  # use a small value to ensure that the total result is positive
    }  # 62 in total

    CACHE = {}
    HIT = 0
    MISS = 0

    def __init__(self, board: Tuple[str], next_side: Role):
        super().__init__(board, next_side)
        self._valid_choices = None
        self._generals = {}
        self._pieces = {}
        self._score = None

    @property
    def feature(self):
        return f"{self._board}{self._next_side}"

    @property
    def score(self):
        if self._score is None:
            self_power = sum(self.SCORE_TABLE[p.lower()] for p in self.pieces(self.next_side).values())
            oppo_power = sum(self.SCORE_TABLE[p.lower()] for p in self.pieces(self.next_side.opponent).values())
            alive_score = 1 if self.general_position(self.next_side) else 0
            self._score = alive_score * self_power / oppo_power
        return self._score

    @property
    def valid_choices(self):
        if self._valid_choices is None:
            self._valid_choices = []
            if self.general_position(self._next_side) is None:
                return self._valid_choices
            vectors = sum(([(k, t) for t in self._targets(k)] for k in self.pieces(self._next_side)), [])
            for v in vectors:
                try:
                    self._valid_choices.append(self.create_from_vector(self.is_valid(v)))
                except RuleViolatedError:
                    pass
        return self._valid_choices

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

    def general_position(self, side: Role):
        if side not in self._generals:
            for i in (0, 1, 2, 7, 8, 9):
                for j in (3, 4, 5):
                    if self[i][j] in GENERAL:
                        if side.iff_func(self[i][j]):
                            self._generals[side] = (i, j)
                            return i, j
                        else:
                            self._generals[side.opponent] = (i, j)
            else:
                self._generals[side] = None
        return self._generals[side]

    def pieces(self, side: Role):
        if side not in self._pieces:
            self._pieces[side] = {}
            for i in range(10):
                for j in range(9):
                    if side.iff_func(self[i][j]):
                        self._pieces[side][(i, j)] = self[i][j]
        return self._pieces[side]

    def _targets(self, tup) -> List[Tuple]:
        piece = self.occupation(tup)
        if fun := TARGETS.get(piece.lower()):
            return fun(tup)
        i, j = tup
        side = SIDE[piece]
        if piece in PAWN:
            pawn_targets = []
            if self.general_position(side)[0] in (0, 1, 2):
                pawn_targets.append((i + 1, j))
                if i >= 5:
                    pawn_targets.extend([(i, j + 1), (i, j - 1)])
            if self.general_position(side)[0] in (7, 8, 9):
                pawn_targets.append((i - 1, j))
                if i <= 4:
                    pawn_targets.extend([(i, j + 1), (i, j - 1)])
            return pawn_targets
        if piece in GENERAL:
            general_targets = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            i_, j_ = self.general_position(side.opponent)
            if j == j_:
                general_targets.append((i_, j_))
            return general_targets
        return []
