from typing import Tuple, List

from constants import Role, DISPLAY, SIDE
from core.errors import *
from core.rules.boundaries import BOUNDARY
from core.rules.paths import PATH
from core.rules.pieces import *
from core.rules.targets import TARGETS


class StateBase:
    CACHE = {}
    HIT = 0
    MISS = 0

    def __init__(self, board: Tuple[str], next_side: Role):
        self._next_side = next_side
        self._board = board
        self._rows = None
        self._cols = None
        self._generals = {}
        self._pieces = {}
        self._valid_choices = None

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item):
        return self._board[item]

    def __hash__(self):
        return hash(self._board) + hash(self._next_side)

    def __eq__(self, other):
        return self._board == other.board and self._next_side == other.next_side

    @property
    def feature(self):
        return f"{self._next_side}{self._board}"

    @property
    def next_side(self):
        return self._next_side

    @property
    def board(self):
        return self._board

    @property
    def rows(self):
        if not self._rows:
            self._rows = [row for row in self._board]
        return self._rows

    @property
    def cols(self):
        if not self._cols:
            self._cols = [''.join(row[j] for row in self.rows) for j in range(9)]
        return self._cols

    @property
    def display(self):
        shift = " " * 50
        lines = ["一二三四五六七八九", *[''.join(DISPLAY[c] for c in row) for row in self.rows], "九八七六五四三二一"]
        return f'\n'.join(shift + line for line in lines)

    def create_from_vector(self, vector):
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        board = [list(line) for line in self]
        board[i_f][j_f] = board[i_s][j_s]
        board[i_s][j_s] = " "
        return self.create_with_cache(tuple(''.join(line) for line in board), self._next_side.opponent)

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

    def occupation(self, tup):
        i, j = tup
        return self[i][j]

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

    def is_valid(self, vector):
        """
        check whether the displacement is performable by ensuring that:
        1. the target is valid (not occupied by own pieces and not exceed bound)
        2. the path is valid (no obstacle for common pieces and one obstacle for cannon)
        If requirement is satisfied, produce the new board in tuple of string format
        """
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        piece_s = self[i_s][j_s]
        if i_f < 0 or i_f > 9 or j_f < 0 or j_f > 8:
            raise ExceedBoundaryError
        if not BOUNDARY[piece_s.lower()](i_f, j_f):
            raise ExceedBoundaryError
        piece_f = self[i_f][j_f]

        if SIDE.get(piece_s, None) == SIDE.get(piece_f, None):
            raise AttackFriendError

        path = ''.join(self.occupation(point) for point in PATH[piece_s.lower()](vector))
        num_of_obstacle = len(path) - path.count(' ')
        if piece_s in CANNON and piece_f != ' ':
            # cannon is attacking, one obstacle should on the path
            if num_of_obstacle != 1:
                raise NoRackError
        else:
            # cannon is not attacking or other pieces is moving or attacking, no obstacle should on the path
            if num_of_obstacle != 0:
                raise PathBlockedError
        return vector
