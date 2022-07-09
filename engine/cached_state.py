from typing import Tuple

from core.role import Role
from engine.evaluable_state import EvaluableState


class CachedState(EvaluableState):
    """
    Using a global instance cache to avoid the same situation calculated multiple time
    """

    CACHE = {}
    HIT = 0
    MISS = 0

    @classmethod
    def from_board_and_role(cls, board: Tuple[str], role: Role) -> 'CachedState':
        feature = (board, role)
        if feature in cls.CACHE:
            cls.HIT += 1
            return cls.CACHE[feature]
        else:
            cls.MISS += 1
            new_state = cls(board=board, current_player=role)
            cls.CACHE[feature] = new_state
            return new_state
