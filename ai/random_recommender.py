import random

from ai.base import Recommender

random.seed(0)


class RandomRecommender(Recommender):
    def strategy(self):
        return random.choice(self._state.legal_choices)
