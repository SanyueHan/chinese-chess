from typing import Tuple, List

from constants import Role, DISPLAY, ENCODE, DECODE, SIDE
from rules.boundaries import BOUNDARY
from rules.paths import PATH
from rules.targets import TARGETS

PAWN = set("pP")
GENERAL = set("gG")
SLOW_PIECES = PAWN | GENERAL
ROOK = set("rR")
CANNON = set("cC")
FAST_PIECES = ROOK | CANNON
STRAIGHT_PIECES = SLOW_PIECES | FAST_PIECES
KNIGHT = set("kK")
MINISTER = set("mM")
ASSISTANT = set("aA")
DIAGONAL_PIECES = KNIGHT | MINISTER | ASSISTANT
PIECES = STRAIGHT_PIECES | DIAGONAL_PIECES


class State:
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

    def parse(self, command):
        """
        Input command, return start coordinate and final coordinate for the movement.
        Check whether the movement is allowed for that kind of piece only,
        without considering the restriction because of the other pieces on the board.
        Raise error if check failed.
        """
        movement = ''.join(ENCODE.get(c, c) for c in command)
        for c in movement:
            if self.next_side.opponent.iff_func(c):
                raise ValueError(f"{DECODE[c]} doesn't belongs to you. ")

        # get start coordinate
        if (piece := movement[0]) in PIECES and (position := movement[1]) in "123456789":
            p = int(position)
            if (n := self.cols[-p].count(piece)) != 1:
                if n == 0:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"no {DECODE[piece]} in column {p}")
                if n > 1:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"multiple {DECODE[piece]} in column {p}")
            i = self.cols[-p].index(piece)
            j = 9 - p

        elif (piece := movement[1]) in PIECES and (position := movement[0]) in "^$":
            for j in range(9):
                col = self.cols[j]
                if col.count(piece) == 2:
                    i = col.find(piece) if position == "^" else col.rfind(piece)
                    break
            else:
                raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                 f"no two {DECODE[piece]} at same column")
        else:
            raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}")
        start = (i, j)

        # command target check
        if movement[2] not in "+-=":
            raise ValueError(f"Invalid command: {movement}, invalid direction. ")
        d = movement[2]
        if movement[3] not in "123456789":
            raise ValueError(f"Invalid command: {movement}, invalid destination. ")
        n = int(movement[3])

        # get final coordinate
        if piece in STRAIGHT_PIECES:
            if d == "+":
                if piece in SLOW_PIECES and n != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                i -= n
            if d == "-":
                if piece in PAWN:
                    raise ValueError(f"{DECODE[piece]} can not move backward. ")
                if piece in GENERAL and n != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                i += n
            if d == "=":
                j = 9 - n
                horizontal_displacement = abs(j - start[1])
                if j == start[1]:
                    raise ValueError(f"Invalid movement: no displacement. ")
                if piece in SLOW_PIECES and horizontal_displacement != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                if piece in PAWN and i > 4:
                    raise ValueError(f"{DECODE[piece]} can not move horizontally before passing the river. ")
        else:
            j = 9 - n
            horizontal_displacement = abs(j - start[1])
            if d == "=":
                raise ValueError(f"Invalid movement for {DECODE[piece]}. ")
            if piece in ASSISTANT:
                if horizontal_displacement != 1:
                    raise ValueError("Invalid movement for assistant. ")
                if d == "+":
                    i -= 1
                if d == "-":
                    i += 1
            if piece in MINISTER:
                if horizontal_displacement != 2:
                    raise ValueError("Invalid movement for minister. ")
                if d == "+":
                    i -= 2
                if d == "-":
                    i += 2
            if piece in KNIGHT:
                if horizontal_displacement not in (1, 2):
                    raise ValueError("Invalid movement for knight. ")
                if d == "+":
                    i -= 1 if horizontal_displacement == 2 else 2
                if d == "-":
                    i += 1 if horizontal_displacement == 2 else 2
        final = (i, j)

        return start, final

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
                except ValueError:
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
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} exceeds boundary. ")
        if not BOUNDARY[piece_s.lower()](i_f, j_f):
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} exceeds boundary. ")
        piece_f = self[i_f][j_f]

        if SIDE.get(piece_s, None) == SIDE.get(piece_f, None):
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} attacks friend. ")

        path = ''.join(self.occupation(point) for point in PATH[piece_s.lower()](vector))
        num_of_obstacle = len(path) - path.count(' ')
        if piece_s in CANNON and piece_f != ' ':
            # cannon is attacking, one obstacle should on the path
            if num_of_obstacle != 1:
                raise ValueError(f"Invalid path for {DECODE[piece_s]}. ")
        else:
            # cannon is not attacking or other pieces is moving or attacking, no obstacle should on the path
            if num_of_obstacle != 0:
                raise ValueError(f"Invalid path for {DECODE[piece_s]}. ")
        return vector
