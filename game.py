from constants import Role, TURN, HELP
from core.state import State
from ai.tree_search_recommender import TreeSearchRecommender


class Game:
    def __init__(self, role=Role.OFFENSIVE, developer_mode=True):
        while role is None:
            role_ = input("Which role do you prefer: OFFENSIVE or DEFENSIVE? \n")
            try:
                role = Role[role_]
            except KeyError:
                print("invalid choice, please input again. ")
        self._recommender = TreeSearchRecommender()
        self._play_modes = {Role.OFFENSIVE: self._machine_move, Role.DEFENSIVE: self._machine_move, role: self._mankind_move}
        self._history = []
        self._winner = None
        self._state = State(role.init, next_side=Role.OFFENSIVE)
        self._dev = developer_mode

    def play(self):
        print(f"Welcome to Chinese Chess! ")
        print(self._state.display)
        while self._winner is None:
            side = TURN[len(self._history) % 2]
            if self._recommender.top_score(self._state, 2) == 0:
                self._winner = side.OPPONENT
                break
            if move := self._play_modes[side]():
                self._history.append(self._state.board)
                self._state = move
                print(move.display)
            else:
                print(f"{side} resigned. ")
                self._winner = side.OPPONENT
            if self._dev:
                print(f"cache hit: {self._state.HIT}")
                print(f"cache miss: {self._state.MISS}")
                print(f"cache size: {len(self._state.CACHE)}")
        print(f"Winner: {self._winner}")

    def _mankind_move(self):
        while True:
            command = input(f"please input your next move: ")
            if command in ("--help", "-h"):
                print(HELP)
                continue
            if command.lower() == "resign":
                self._winner = self._state.next_side.OPPONENT
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
        result = self._recommender.strategy(self._state)
        return result
