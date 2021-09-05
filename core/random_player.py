import random


from core.state import State


random.seed(0)


class RandomPlayer(State):
    def strategy(self):
        return random.choice(self.legal_choices)
