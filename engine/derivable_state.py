from typing import List, Union

from TimeAnalyzer.metaclass import TimeAnalyzer
from core import StateBase
from core.role import Role, get_role
from core.rules.pieces import *
from core.rules.targets import TARGETS


class DerivableState(StateBase, metaclass=TimeAnalyzer):
    """
    DerivableState provide an interface that returns all the valid children state in the current situation,
    which could be used to generate a search tree.
    The 'valid' means that those movements conform to the basic rules of Chinese Chess.
    Whether this move cause the player losing its general in next step is not considered.
    (in game logic level this kind of movement is forbidden by a one-step-derivation, but here it's not considered)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = None
        self.__generals = {}
        self.__pieces = {}

    @property
    def children(self) -> List['DerivableState']:
        if self._children is None:
            self._get_children()
        return self._children

    def from_vector(self, vector) -> 'DerivableState':
        new_state = super().from_vector(vector)
        source, target = vector
        if self_pieces := self.__pieces.get(self._current_player):
            new_self_pieces = self_pieces.copy()
            new_self_pieces[target] = new_self_pieces.pop(source)
            new_state.__pieces[self._current_player] = new_self_pieces
        if oppo_pieces := self.__pieces.get(self._current_player.opponent):
            new_oppo_pieces = oppo_pieces.copy()
            new_oppo_pieces.pop(target, None)
            new_state.__pieces[self._current_player.opponent] = new_oppo_pieces
        return new_state

    def get_child(self, index: int) -> 'DerivableState':
        return self._children[index]

    def _get_children(self):
        self._children = []
        if self._get_general_position(self._current_player):
            for source in self._get_pieces(self._current_player):
                for target in self._get_targets(source):
                    vector = (source, target)
                    if self.is_valid(vector):
                        self._children.append(self.from_vector(vector))

    def _get_general_position(self, side: Role) -> Union[tuple, None]:
        if side not in self.__generals:
            for i in (0, 1, 2, 7, 8, 9):
                for j in (3, 4, 5):
                    if self._board[i][j] in GENERAL:
                        if side.iff_func(self._board[i][j]):
                            self.__generals[side] = (i, j)
                            return i, j
                        else:
                            self.__generals[side.opponent] = (i, j)
            else:
                self.__generals[side] = None
        return self.__generals[side]

    def _get_pieces(self, side: Role) -> dict:
        if side not in self.__pieces:
            self.__pieces[side] = {}
            for i in range(10):
                for j in range(9):
                    if side.iff_func(self._board[i][j]):
                        self.__pieces[side][(i, j)] = self._board[i][j]
        return self.__pieces[side]

    def _get_targets(self, pos) -> List[tuple]:
        piece = self._occupation(pos)
        if fun := TARGETS.get(piece.lower()):
            return fun(pos)
        i, j = pos
        side = get_role(piece)
        if piece in PAWN:
            pawn_targets = []
            if self._get_general_position(side)[0] in (0, 1, 2):
                pawn_targets.append((i + 1, j))
                if i >= 5:
                    pawn_targets.extend([(i, j + 1), (i, j - 1)])
            if self._get_general_position(side)[0] in (7, 8, 9):
                pawn_targets.append((i - 1, j))
                if i <= 4:
                    pawn_targets.extend([(i, j + 1), (i, j - 1)])
            return pawn_targets
        if piece in GENERAL:
            general_targets = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            i_, j_ = self._get_general_position(side.opponent)
            if j == j_:
                general_targets.append((i_, j_))
            return general_targets
        return []
