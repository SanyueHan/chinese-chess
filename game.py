from constants import Role, TURN
from constants.help import HELP
from core.ai_players import *


STRATEGIES = {
    0: RandomPlayer
}


class Game:
    def __init__(self, role, ai_level, developer_mode=False):
        self._state = STRATEGIES[ai_level](role.init, next_side=Role.OFFENSIVE)
        self._play_modes = {
            Role.OFFENSIVE: self._machine_move,
            Role.DEFENSIVE: self._machine_move
        }
        if isinstance(role, Role):
            self._play_modes[role] = self._mankind_move
        self._history = []
        self._winner = None
        self._dev = developer_mode

    def play(self):
        print(f"Welcome to Chinese Chess! ")
        print(self._state.display)
        while self._winner is None:
            side = TURN[len(self._history) % 2]
            if not self._state.legal_choices:
                self._winner = side.OPPONENT
                break
            self._play_modes[side]()
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
                pass
            try:
                vector = self._state.parse(command)
                vector = self._state.is_valid(vector)
                result = self._state.create_from_vector(vector)
                result.is_legal()
                self._history.append(self._state.board)
                self._state = result
                break
            except ValueError as err:
                print(err)
                print("Enter --help or -h for help. ")
                continue
        print(self._state.display)

    def _machine_move(self):
        print("Machine is thinking...")
        result = self._state.strategy()
        self._history.append(self._state.board)
        self._state = result
        print(self._state.display)
