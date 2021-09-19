from ai.base import Recommender
from ai.score_recommender import ScoreRecommender
from cache import cache


get_score = ScoreRecommender().score


class Node:
    def __init__(self, state):
        self._state = state
        self._children = []

    def build(self, depth):
        if depth:
            self._children = [Node(state) for state in cache.legal_movements(self._state)]
            for child in self._children:
                child.build(depth - 1)

    def search(self, pick=False):
        if not self._children:
            return self._state
        choices = [child.search() for child in self._children]
        choice_scores = [(get_score(choice), choice) for choice in choices]
        choice_scores = [(v, s) if s.next_side == self._state.next_side else (self.reciprocal(v), s)
                         for v, s in choice_scores]
        best = max(choice_scores, key=lambda tup: tup[0])
        if pick:
            index = choice_scores.index(best)
            return self._children[index].state
        else:
            return best[1]

    @staticmethod
    def reciprocal(score):
        if score:
            return 1/score
        return float('inf')

    @property
    def state(self):
        return self._state


class TreeSearchRecommender(Recommender):
    DEPTH = 2

    def strategy(self, state):
        root = Node(state)
        root.build(self.DEPTH)
        return root.search(True)
