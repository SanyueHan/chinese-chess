from typing import Union

from engine.cached_state import CachedState
from utils.decorators import time_debugger, generate_debugger


space_debugger = generate_debugger(CachedState.debug_cache)


class TreeSearcher:
    def __init__(self, depth: int):
        assert depth > 0
        self._depth: int = depth

    @space_debugger
    @time_debugger
    def get_best_recommendation(self, serialized_state: str) -> str:
        root = CachedState.from_string(serialized_state)
        self._build(state=root, depth=self._depth)
        index, best_result = self._search(state=root, depth=self._depth)
        return root.get_child(index).to_string()

    def get_top_score(self, serialized_state: str) -> (int, int):
        root = CachedState.from_string(serialized_state)
        self._build(state=root, depth=self._depth)
        _, best_result = self._search(state=root, depth=self._depth)
        if self._depth % 2:
            return self.__get_opposite_vector(best_result.score)
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
                result_scores[res] = self.__get_opposite_vector(res.score)
        best_result = max(result_scores, key=result_scores.get)
        return list(result_scores.keys()).index(best_result), best_result

    @staticmethod
    def __get_opposite_vector(score):
        return tuple(-s for s in score)
