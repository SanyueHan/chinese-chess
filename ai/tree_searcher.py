from ai.state_for_machine import StateForMachine
from config import DEVELOPER_MODE


class Node:
    def __init__(self, state):
        self._state = state
        self._children = []

    def build(self, depth):
        if depth:
            self._children = [Node(state) for state in self._state.valid_choices]
            for child in self._children:
                child.build(depth - 1)

    def search(self):
        """
        :return: the index of the child who returns the top score, the top score, the result that gives the top score
        """
        if not self._children:
            return None, None, self._state
        choices = [child.search()[2] for child in self._children]
        choices = [(choice.score, choice) for choice in choices]
        choices = [(v, s) if s.next_side == self._state.next_side else (self.reciprocal(v), s) for v, s in choices]
        best = max(choices, key=lambda tup: tup[0])
        return choices.index(best), best[0], best[1]

    def get_child(self, index):
        return self._children[index]

    @staticmethod
    def reciprocal(score):
        if score:
            return 1/score
        return float('inf')

    @property
    def state(self):
        return self._state


class TreeSearcher:
    def __init__(self, depth):
        self._depth = depth

    def strategy(self, board, next_side):
        root = Node(StateForMachine(board, next_side))
        root.build(self._depth)
        index, score, result = root.search()
        if DEVELOPER_MODE:
            print(f"The best score for {next_side} in a search of depth {self._depth} is {score}")
        return root.get_child(index).state

    def top_score(self, board, next_side):
        root = Node(StateForMachine(board, next_side))
        root.build(self._depth)
        return root.search()[1]
