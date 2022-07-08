from typing import Tuple

from ai.cached_state import CachedState
from config import DEVELOPER_MODE


class TreeSearcher:
    def __init__(self, depth):
        self._depth = depth

    def get_best_recommendation(self, board, next_side) -> Tuple[str]:
        root = CachedState(board, next_side)
        self._build(root, self._depth)
        index, score, result = self._search(root, self._depth)
        if DEVELOPER_MODE:
            print(f"The best score for {next_side} in a search of depth {self._depth} is {score}")
            print(f"cache hit: {CachedState.HIT}")
            print(f"cache miss: {CachedState.MISS}")
            print(f"cache size: {len(CachedState.CACHE)}")
        return root.get_child(index).board

    def get_top_score(self, board, next_side):
        root = CachedState(board, next_side)
        self._build(root, self._depth)
        return self._search(root, self._depth)[1]

    def _build(self, state, depth):
        if depth:
            for child in state.children:
                self._build(child, depth-1)

    def _search(self, state, depth):
        if depth == 0 or not state.children:
            return None, None, state
        choices = [self._search(child, depth-1)[2] for child in state.children]
        choices = [(choice.score, choice) for choice in choices]
        choices = [(v, s) if s.next_side == state.next_side else (self.__get_reciprocal_value(v), s) for v, s in choices]
        best = max(choices, key=lambda tup: tup[0])
        return choices.index(best), best[0], best[1]

    @staticmethod
    def __get_reciprocal_value(score):
        if score:
            return 1 / score
        return float('inf')
