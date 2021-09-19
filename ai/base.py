from abc import ABCMeta, abstractmethod


class Recommender(metaclass=ABCMeta):
    @abstractmethod
    def strategy(self, state):
        pass
