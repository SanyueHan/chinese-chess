from typing import Tuple

from core.consts.coding import decode, encode
from core.errors import *
from core.role import Role, get_role
from core.rules.boundaries import BOUNDARY
from core.rules.paths import PATH
from core.rules.pieces import CANNON


class StateBase:
    def __init__(self, board: Tuple[str], current_player: Role):
        self._board: Tuple[str] = board
        self._current_player: Role = current_player
        self.__cols = None

    def __getitem__(self, item):
        return self._board[item]

    def __iter__(self):
        return iter(self._board)

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

    @property
    def board(self) -> Tuple[str]:
        return self._board

    @property
    def current_player(self) -> Role:
        return self._current_player

    @classmethod
    def from_board_and_role(cls, board: Tuple[str], role: Role) -> 'StateBase':
        return cls(board=board, current_player=role)

    @classmethod
    def from_string(cls, string: str) -> 'StateBase':
        lines = string.split('\n')
        current_player = Role[lines.pop()]
        assert len(lines) == 10
        assert all(len(line) == 9 for line in lines)
        board = tuple(encode(line) for line in lines)
        return cls(
            board=board,
            current_player=current_player
        )

    def from_vector(self, vector) -> 'StateBase':
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        board = [list(line) for line in self]
        board[i_f][j_f] = board[i_s][j_s]
        board[i_s][j_s] = " "
        return self.from_board_and_role(
            board=tuple(''.join(line) for line in board),
            role=self._current_player.opponent
        )

    def to_string(self, dec=True) -> str:
        if dec:
            return '\n'.join(decode(line) for line in self._board) + '\n' + self._current_player.name
        else:
            return '\n'.join(self._board) + '\n' + self._current_player.name

    def is_valid(self, vector) -> bool:
        try:
            self.check_validity(vector)
            return True
        except RuleViolatedError:
            return False

    def check_validity(self, vector) -> Tuple[tuple]:
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

        path = ''.join(self._occupation(point) for point in PATH[piece_s.lower()](vector))
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

    @property
    def _rows(self) -> Tuple[str]:
        return self._board

    @property
    def _cols(self) -> Tuple[str]:
        if not self.__cols:
            self.__cols = tuple(''.join(row[j] for row in self._rows) for j in range(9))
        return self.__cols

    def _occupation(self, tup):
        i, j = tup
        return self[i][j]
