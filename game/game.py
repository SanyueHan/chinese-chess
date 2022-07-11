from config import AI_SEARCH_DEPTH
from core.consts.boards import DEFENSIVE_DOWN, OFFENSIVE_DOWN
from core.errors import RuleViolatedError
from core.role import Role
from game.errors import InvalidCommandError
from game.state_for_mankind import StateForMankind
from engine import TreeSearcher


FOOL_PROOFER = TreeSearcher(1)
REFEREE = TreeSearcher(2)
AI = TreeSearcher(AI_SEARCH_DEPTH)


class Game:
    def __init__(self, role=Role.OFFENSIVE):
        while role is None:
            role_ = input("Which role do you prefer: OFFENSIVE or DEFENSIVE? \n")
            try:
                role = Role[role_]
            except KeyError:
                print("invalid choice, please input again. ")
        board = OFFENSIVE_DOWN if role is Role.OFFENSIVE else DEFENSIVE_DOWN
        self._play_modes = {Role.OFFENSIVE: self._machine_move, Role.DEFENSIVE: self._machine_move, role: self._mankind_move}
        self._history = []
        self._winner = None
        self._state = StateForMankind(board, current_player=Role.OFFENSIVE)

    def play(self):
        print(f"Welcome to Chinese Chess! ")
        print(self._state.display)
        while self._winner is None:
            side = self._state.current_player
            if REFEREE.get_top_score(self._state.to_string())[0] == -1:
                # if no matter how the current player move the opponent could always kill his/her/its general,
                # the referee will judge the current player as the loser
                self._winner = side.opponent
                break
            if move := self._play_modes[side]():
                self._history.append(self._state.board)
                self._state = move
                print(move.display)
            else:
                print(f"{side} resigned. ")
                self._winner = side.opponent
        print(f"Winner: {self._winner}")

    def _mankind_move(self):
        while True:
            command = input(f"please input your next move: ")
            if command.lower() == "resign":
                return
            if command.lower() == "revert":
                if len(self._history) >= 2:
                    self._history.pop()
                    self._state = StateForMankind(self._history.pop(), self._state.current_player)
                    print("Reverted to two steps before. ")
                    print(self._state.display)
                else:
                    print("Unable to revert. ")
                continue
            try:
                vector = self._state.parse_command(command)
            except InvalidCommandError as err:
                print(err)
                print("See README.md for command format. ")
                continue
            try:
                self._state.check_validity(vector)
            except RuleViolatedError as err:
                print(err)
                continue
            result = self._state.from_vector(vector)
            if FOOL_PROOFER.get_top_score(result.to_string())[0] == 1:
                # opponent could kill your general in one step if this movement is taken,
                # indicating the player may enter a stupid command.
                # forbid this action and ask the player to choose another one
                # (The REFEREE didn't announce that you have lost the game, means better choice exists)
                print("Invalid movement - general will be killed! ")
            else:
                return result

    def _machine_move(self):
        print("Machine is thinking...")
        return StateForMankind.from_string(AI.get_best_recommendation(self._state.to_string()))
