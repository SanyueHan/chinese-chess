from typing import List, Union

from time_analyzer.metaclass import TimeAnalyzer

from core import StateBase
from core.role import Role, get_role
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

    def from_vector(self, vector: (int, int)) -> 'DerivableState':
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

    def _get_general_position(self, side: Role) -> Union[int, None]:
        if side not in self.__generals:
            for i in (0, 1, 2, 7, 8, 9):
                for j in (3, 4, 5):
                    index = i * 9 + j
                    if self._board[index].upper() == 'G':
                        if side.iff_func(self._board[index]):
                            self.__generals[side] = index
                            return index
                        else:
                            self.__generals[side.opponent] = index
            else:
                self.__generals[side] = None
        return self.__generals[side]

    def _get_pieces(self, side: Role) -> dict:
        if len(self.__pieces) == 0:
            self_d = self.__pieces[self._current_player] = {}
            oppo_d = self.__pieces[self._current_player.opponent] = {}
            for i in range(90):
                if self._board[i].isalpha():
                    if self._current_player.iff_func(self._board[i]):
                        self_d[i] = self._board[i]
                    else:
                        oppo_d[i] = self._board[i]
        return self.__pieces[side]

    def _get_targets(self, source: int) -> List[int]:
        piece = self._board[source]
        if fun := TARGETS.get(piece.lower()):
            return fun(source)
        side = get_role(piece)
        if piece.upper() == 'P':
            pawn_targets = []
            if self._get_general_position(side) // 9 in (0, 1, 2):
                pawn_targets.append(source + 9)
                if source // 9 >= 5:
                    pawn_targets.extend([source + 1, source - 1])
            if self._get_general_position(side) // 9 in (7, 8, 9):
                pawn_targets.append(source - 9)
                if source // 9 <= 4:
                    pawn_targets.extend([source + 1, source - 1])
            return pawn_targets
        if piece.upper() == 'G':
            general_targets = [source + 9, source - 9, source + 1, source - 1]
            opponent_general_index = self._get_general_position(side.opponent)
            if opponent_general_index % 9 == source % 9:
                general_targets.append(opponent_general_index)
            return general_targets
        return []
