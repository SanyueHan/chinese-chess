from typing import Tuple

from constants import Role, DISPLAY

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


class Board:
    M = 10
    N = 9

    def __init__(self, board: Tuple[str], next_side: Role):
        self._next_side = next_side
        self._board = board
        self._rows = None
        self._cols = None
        self._generals = {}

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item):
        return self._board[item]

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
            self._cols = [''.join(row[j] for row in self.rows) for j in range(self.N)]
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
        return self.__class__(tuple(''.join(line) for line in board), self._next_side.OPPONENT)

    @classmethod
    def create_from_board(cls, board, next_side):
        return cls(board, next_side)

    def _occupation(self, tup):
        i, j = tup
        return self[i][j]

    @staticmethod
    def _side(piece):
        if piece.islower():
            return Role.OFFENSIVE
        if piece.isupper():
            return Role.DEFENSIVE

    def _general_position(self, side: Role):
        if side not in self._generals:
            for i in (0, 1, 2, 7, 8, 9):
                for j in (3, 4, 5):
                    if self[i][j] in GENERAL:
                        if side.func(self[i][j]):
                            self._generals[side] = (i, j)
                            break
                        else:
                            self._generals[side.OPPONENT] = (i, j)
        try:
            return self._generals[side]
        except KeyError as e:
            print(self.display)
            raise e

