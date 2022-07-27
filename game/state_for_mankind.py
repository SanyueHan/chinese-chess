from core.consts.coding import DECODE, ENCODE
from core import StateBase
from game.display import DISPLAY
from game.errors import InvalidCommandError
from game.pieces import *
from game.regex import CN2NUM, COMMAND_PATTERN_1, COMMAND_PATTERN_2


class StateForMankind(StateBase):
    @property
    def display(self) -> str:
        shift = " " * 50
        lines = ["一二三四五六七八九", *[''.join(DISPLAY[c] for c in row) for row in self._rows], "九八七六五四三二一"]
        return f'\n'.join(shift + line for line in lines)

    def parse_command(self, movement: str) -> (int, int):
        """
        Input command, return start coordinate and final coordinate for the movement.
        Check whether the movement is allowed for that kind of piece only,
        without considering the restriction because of the other pieces on the board.
        Raise error if check failed.
        """

        # todo: auto correct 象/相 according to current player

        if match := COMMAND_PATTERN_1.fullmatch(movement):
            source = self._parse_source_1(match.group(1))
            target = self._parse_target(source, match.group(2))
            return source, target
        elif match := COMMAND_PATTERN_2.fullmatch(movement):
            source = self._parse_source_2(match.group(1))
            target = self._parse_target(source, match.group(2))
            return source, target
        else:
            raise InvalidCommandError

    def _parse_source_1(self, description) -> int:
        piece_cn = description[0]
        position = description[1]
        piece = ENCODE[piece_cn]
        j = 9 - CN2NUM[position]
        n = self._cols[j].count(piece)
        if n == 0:
            raise InvalidCommandError(f"Invalid command: no {piece_cn} in column {position}")
        if n > 1:
            raise InvalidCommandError(f"Invalid command: multiple {piece_cn} in column {position}")
        return self._cols[j].index(piece) * 9 + j

    def _parse_source_2(self, description) -> int:
        position = description[0]
        piece_cn = description[1]
        piece = ENCODE[piece_cn]
        for j in range(9):
            col = self._cols[j]
            if col.count(piece) == 2:
                i = col.find(piece) if position == "前" else col.rfind(piece)
                return i * 9 + j
        else:
            raise InvalidCommandError(f"Invalid command: no two {piece_cn} at same column")

    def _parse_target(self, source, action) -> int:
        piece = self._board[source]
        i = source // 9
        j = source % 9

        d = action[0]
        n = CN2NUM[action[1]]

        # get final coordinate
        if piece in STRAIGHT_PIECES:
            if d == "进":
                if piece in SLOW_PIECES and n != 1:
                    raise InvalidCommandError(f"{DECODE[piece]} can only move one unit. ")
                return (i - n) * 9 + j
            if d == "退":
                if piece in PAWN:
                    raise InvalidCommandError(f"{DECODE[piece]} can not move backward. ")
                if piece in GENERAL and n != 1:
                    raise InvalidCommandError(f"{DECODE[piece]} can only move one unit. ")
                return (i + n) * 9 + j
            if d == "平":
                j_ = 9 - n
                horizontal_displacement = abs(j - j_)
                if horizontal_displacement == 0:
                    raise InvalidCommandError(f"Invalid movement: no displacement. ")
                if piece in SLOW_PIECES and horizontal_displacement != 1:
                    raise InvalidCommandError(f"{DECODE[piece]} can only move one unit. ")
                if piece in PAWN and i > 4:
                    raise InvalidCommandError(f"{DECODE[piece]} can not move horizontally before passing the river. ")
                return i * 9 + j_
        else:
            j_ = 9 - n
            horizontal_displacement = abs(j - j_)
            if d == "平":
                raise InvalidCommandError(f"Invalid movement for {DECODE[piece]}. ")
            if piece in ASSISTANT:
                if horizontal_displacement != 1:
                    raise InvalidCommandError("Invalid movement for assistant. ")
                if d == "进":
                    return (i - 1) * 9 + j_
                if d == "退":
                    return (i + 1) * 9 + j_
            if piece in MINISTER:
                if horizontal_displacement != 2:
                    raise InvalidCommandError("Invalid movement for minister. ")
                if d == "进":
                    return (i - 2) * 9 + j_
                if d == "退":
                    return (i + 2) * 9 + j_
            if piece in KNIGHT:
                if horizontal_displacement not in (1, 2):
                    raise InvalidCommandError("Invalid movement for knight. ")
                vertical_displacement = 1 if horizontal_displacement == 2 else 2
                if d == "进":
                    return (i - vertical_displacement) * 9 + j_
                if d == "退":
                    return (i + vertical_displacement) * 9 + j_
