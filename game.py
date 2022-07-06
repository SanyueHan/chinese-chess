import os
import time

from constants import Role, HELP, DEVELOPER_MODE, BOARDS
from core.state import State
from ai.tree_search_recommender import TreeSearchRecommender


BOARD_MAP_FOR_HUMAN_ROLES = {
    Role.OFFENSIVE: BOARDS["OFFENSIVE"],
    Role.DEFENSIVE: BOARDS["DEFENSIVE"]
}


class Game:
    def __init__(self, role=Role.OFFENSIVE, board=None):
        while role is None:
            role_ = input("Which role do you prefer: OFFENSIVE or DEFENSIVE? \n")
            try:
                role = Role[role_]
            except KeyError:
                print("invalid choice, please input again. ")
        if board is None:
            if board := os.environ.get("BOARD"):
                board = BOARDS[board]
            else:
                board = BOARD_MAP_FOR_HUMAN_ROLES[role]
        self._recommender = TreeSearchRecommender()
        self._play_modes = {Role.OFFENSIVE: self._machine_move, Role.DEFENSIVE: self._machine_move, role: self._mankind_move}
        self._history = []
        self._winner = None
        self._state = State(board, next_side=Role.OFFENSIVE)

    def play(self):
        print(f"Welcome to Chinese Chess! ")
        print(self._state.display)
        while self._winner is None:
            side = self._state.next_side
            if self._recommender.top_score(self._state, 2) == 0:
                self._winner = side.opponent
                break
            if move := self._play_modes[side]():
                self._history.append(self._state.board)
                self._state = move
                print(move.display)
            else:
                print(f"{side} resigned. ")
                self._winner = side.opponent
            if DEVELOPER_MODE:
                print(f"cache hit: {self._state.HIT}")
                print(f"cache miss: {self._state.MISS}")
                print(f"cache size: {len(self._state.CACHE)}")
        print(f"Winner: {self._winner}")

    def _mankind_move(self):
        while True:
            command = input(f"please input your next move: ")
            if command.lower() == "resign":
                return
            if command.lower() == "revert":
                if len(self._history) >= 2:
                    self._history.pop()
                    self._state = State.create_with_cache(self._history.pop(), self._state.next_side)
                    print("Reverted to two steps before. ")
                    print(self._state.display)
                else:
                    print("Unable to revert. ")
                continue
            if command == 'help' or len(command) not in (4, 5):
                print(HELP)
                continue
            try:
                vector = self._state.parse(command)
                vector = self._state.is_valid(vector)
                result = self._state.create_from_vector(vector)
                if self._recommender.top_score(result, 1) == float('inf'):
                    raise ValueError(f"Invalid movement: General will be killed. ")
                return result
            except ValueError as err:
                print(err)
                print("Enter --help or -h for help. ")
                continue

    def _machine_move(self):
        print("Machine is thinking...")
        time_s = time.time()
        result = self._recommender.strategy(self._state)
        time_e = time.time()
        if DEVELOPER_MODE:
            print(f"Time: {time_e-time_s}")
        return result
