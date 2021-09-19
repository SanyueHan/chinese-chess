import random

from ai.base import Recommender
from cache import cache

random.seed(0)


class RandomRecommender(Recommender):
    def strategy(self, state):
        return random.choice(cache.legal_movements(state))
