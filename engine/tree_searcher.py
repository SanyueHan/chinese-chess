import sys
from typing import Tuple, Union

from config import DEVELOPER_MODE
from core.role import Role
from engine.cached_state import CachedState


class TreeSearcher:
    def __init__(self, depth: int):
        assert depth > 0
        self._depth: int = depth

    def get_best_recommendation(self, board: Tuple[str], current_player: Role) -> Tuple[str]:
        root = CachedState(board=board, current_player=current_player)
        self._build(state=root, depth=self._depth)
        index, best_result = self._search(state=root, depth=self._depth)
        if DEVELOPER_MODE:
            print(f"The best score for {current_player} in a search of depth {self._depth} is {best_result.score}")
            print(f"cache hit: {CachedState.HIT}")
            print(f"cache miss: {CachedState.MISS}")
            print(f"cache size (KB): {CachedState.CACHE.__sizeof__() // 1000}")
            print(f"cache size (KB): {sys.getsizeof(CachedState.CACHE) // 1000}")
        return root.get_child(index).board

    def get_top_score(self, board: Tuple[str], current_player: Role) -> float:
        root = CachedState(board=board, current_player=current_player)
        self._build(state=root, depth=self._depth)
        _, best_result = self._search(state=root, depth=self._depth)
        if self._depth % 2:
            return self.__get_reciprocal_value(best_result.score)
        else:
            return best_result.score

    def _build(self, state, depth: int):
        if depth:
            for child in state.children:
                self._build(child, depth-1)

    def _search(self, state, depth: int) -> (Union[None, int], CachedState):
        """
        :param state:
        :param depth:
        :return: from which branch the best state comes, the best state
        """
        if depth == 0 or not state.children:
            return None, state
        results = [self._search(child, depth-1)[1] for child in state.children]
        result_scores = {}
        for res in results:
            if res.current_player is state.current_player:
                result_scores[res] = res.score
            else:
                result_scores[res] = self.__get_reciprocal_value(res.score)
        best_result = max(result_scores, key=result_scores.get)
        return list(result_scores.keys()).index(best_result), best_result

    @staticmethod
    def __get_reciprocal_value(score):
        if score:
            return 1 / score
        return float('inf')
