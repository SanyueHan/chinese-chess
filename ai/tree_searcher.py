from typing import Tuple

from ai.cached_state import CachedState
from config import DEVELOPER_MODE


class TreeSearcher:
    def __init__(self, depth):
        self._depth = depth

    def get_best_recommendation(self, board, next_side) -> Tuple[str]:
        root = CachedState(board, next_side)
        self._build(root, self._depth)
        index, best_result = self._search(root, self._depth)
        if DEVELOPER_MODE:
            print(f"The best score for {next_side} in a search of depth {self._depth} is {best_result.score}")
            print(f"cache hit: {CachedState.HIT}")
            print(f"cache miss: {CachedState.MISS}")
            print(f"cache size: {len(CachedState.CACHE)}")
        return root.get_child(index).board

    def get_top_score(self, board, next_side):
        root = CachedState(board, next_side)
        self._build(root, self._depth)
        _, best_result = self._search(root, self._depth)
        if self._depth % 2:
            return self.__get_reciprocal_value(best_result.score)
        else:
            return best_result.score

    def _build(self, state, depth):
        if depth:
            for child in state.children:
                self._build(child, depth-1)

    def _search(self, state, depth):
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
            if res.next_side is state.next_side:
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
