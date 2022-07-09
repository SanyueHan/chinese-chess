from typing import Tuple

from core.errors import *
from core.role import Role, get_role
from core.rules.boundaries import BOUNDARY
from core.rules.paths import PATH
from core.rules.pieces import CANNON


class StateBase:
    def __init__(self, board: Tuple[str], next_side: Role):
        self._current_player = next_side
        self._board = board
        self._rows = None
        self._cols = None

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item):
        return self._board[item]

    @property
    def current_player(self):
        return self._current_player

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

    @classmethod
    def from_board_and_role(cls, board, role):
        return cls(board, role)

    def create_from_vector(self, vector):
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        board = [list(line) for line in self]
        board[i_f][j_f] = board[i_s][j_s]
        board[i_s][j_s] = " "
        return self.from_board_and_role(tuple(''.join(line) for line in board), self._current_player.opponent)

    def occupation(self, tup):
        i, j = tup
        return self[i][j]

    def is_valid(self, vector) -> bool:
        try:
            self.check_validity(vector)
            return True
        except RuleViolatedError:
            return False

    def check_validity(self, vector) -> Tuple:
        """
        check whether the displacement is performable by ensuring that:
        1. the target is valid (not occupied by own pieces and not exceed bound)
        2. the path is valid (no obstacle for common pieces and one obstacle for cannon)
        If any rule is violated, raise an error,
        otherwise, return the same vector
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

        if get_role(piece_s) == get_role(piece_f):
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
