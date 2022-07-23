from typing import Tuple

from TimeAnalyzer.metaclass import TimeAnalyzer
from core.consts.coding import decode, encode
from core.errors import *
from core.role import Role, get_role
from core.rules.boundaries import BOUNDARY
from core.rules.paths import PATH
from core.rules.pieces import CANNON


class StateBase(metaclass=TimeAnalyzer):
    def __init__(self, board: str, current_player: Role):
        self._board: str = board
        self._current_player: Role = current_player
        self.__rows = None
        self.__cols = None

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

    @property
    def board(self) -> str:
        return self._board

    @property
    def current_player(self) -> Role:
        return self._current_player

    @classmethod
    def from_string(cls, string: str) -> 'StateBase':
        lines = string.split('\n')
        current_player = Role[lines.pop()]
        assert len(lines) == 10
        assert all(len(line) == 9 for line in lines)
        board = ''.join(encode(line) for line in lines)
        return cls(
            board=board,
            current_player=current_player
        )

    def from_vector(self, vector: (int, int)):
        start, final = vector
        board_new = list(self._board)
        board_new[final] = board_new[start]
        board_new[start] = ' '
        return self.__class__(
            board=''.join(board_new),
            current_player=self._current_player.opponent
        )

    def to_string(self, dec=True) -> str:
        if dec:
            return '\n'.join(decode(line) for line in self._rows) + '\n' + self._current_player.name
        else:
            return '\n'.join(self._rows) + '\n' + self._current_player.name

    def is_valid(self, vector: (int, int)) -> bool:
        try:
            self.check_validity(vector)
            return True
        except RuleViolatedError:
            return False

    def check_validity(self, vector: (int, int)) -> (int, int):
        """
        check whether the displacement is performable by ensuring that:
        1. the target is valid (not occupied by own pieces and not exceed bound)
        2. the path is valid (no obstacle for common pieces and one obstacle for cannon)
        If any rule is violated, raise an error,
        otherwise, return the same vector
        """
        start, final = vector
        if not 0 <= start <= 89 or not 0 <= final <= 89:
            raise ExceedBoardError
        piece_s = self._board[start]
        if not BOUNDARY[piece_s.lower()](final):
            raise ExceedBoundaryError
        piece_f = self._board[final]

        if get_role(piece_s) == get_role(piece_f):
            raise AttackFriendError

        path = ''.join(self._board[point] for point in PATH[piece_s.lower()](vector))
        num_of_obstacle = len(path) - path.count(' ')
        if piece_s in CANNON and piece_f != ' ':
            # cannon is attacking, one obstacle should on the path
            if num_of_obstacle != 1:
                raise NotOneRackError
        else:
            # cannon is not attacking or other pieces is moving or attacking, no obstacle should on the path
            if num_of_obstacle != 0:
                raise PathBlockedError
        return vector

    @property
    def _rows(self) -> Tuple[str]:
        if not self.__rows:
            self.__rows = tuple(self._board[i*9:(i+1)*9] for i in range(10))
        return self.__rows

    @property
    def _cols(self) -> Tuple[str]:
        if not self.__cols:
            self.__cols = tuple(''.join(row[j] for row in self._rows) for j in range(9))
        return self.__cols
