from core.consts.coding import DECODE, encode
from core.rules.pieces import *
from core import StateBase
from game.display import DISPLAY


class StateForMankind(StateBase):
    @property
    def display(self) -> str:
        shift = " " * 50
        lines = ["一二三四五六七八九", *[''.join(DISPLAY[c] for c in row) for row in self._rows], "九八七六五四三二一"]
        return f'\n'.join(shift + line for line in lines)

    def parse_command(self, command: str) -> (int, int):
        """
        Input command, return start coordinate and final coordinate for the movement.
        Check whether the movement is allowed for that kind of piece only,
        without considering the restriction because of the other pieces on the board.
        Raise error if check failed.
        """
        movement = encode(command)
        for c in movement:
            if self.current_player.opponent.iff_func(c):
                raise ValueError(f"{DECODE[c]} doesn't belongs to you. ")

        # get start coordinate
        if (piece := movement[0]) in PIECES and (position := movement[1]) in "123456789":
            p = int(position)
            if (n := self._cols[-p].count(piece)) != 1:
                if n == 0:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"no {DECODE[piece]} in column {p}")
                if n > 1:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"multiple {DECODE[piece]} in column {p}")
            i = self._cols[-p].index(piece)
            j = 9 - p

        elif (piece := movement[1]) in PIECES and (position := movement[0]) in "^$":
            for j in range(9):
                col = self._cols[j]
                if col.count(piece) == 2:
                    i = col.find(piece) if position == "^" else col.rfind(piece)
                    break
            else:
                raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                 f"no two {DECODE[piece]} at same column")
        else:
            raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}")
        start = (i, j)

        # command target check
        if movement[2] not in "+-=":
            raise ValueError(f"Invalid command: {movement}, invalid direction. ")
        d = movement[2]
        if movement[3] not in "123456789":
            raise ValueError(f"Invalid command: {movement}, invalid destination. ")
        n = int(movement[3])

        # get final coordinate
        if piece in STRAIGHT_PIECES:
            if d == "+":
                if piece in SLOW_PIECES and n != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                i -= n
            if d == "-":
                if piece in PAWN:
                    raise ValueError(f"{DECODE[piece]} can not move backward. ")
                if piece in GENERAL and n != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                i += n
            if d == "=":
                j = 9 - n
                horizontal_displacement = abs(j - start[1])
                if j == start[1]:
                    raise ValueError(f"Invalid movement: no displacement. ")
                if piece in SLOW_PIECES and horizontal_displacement != 1:
                    raise ValueError(f"{DECODE[piece]} can only move one unit. ")
                if piece in PAWN and i > 4:
                    raise ValueError(f"{DECODE[piece]} can not move horizontally before passing the river. ")
        else:
            j = 9 - n
            horizontal_displacement = abs(j - start[1])
            if d == "=":
                raise ValueError(f"Invalid movement for {DECODE[piece]}. ")
            if piece in ASSISTANT:
                if horizontal_displacement != 1:
                    raise ValueError("Invalid movement for assistant. ")
                if d == "+":
                    i -= 1
                if d == "-":
                    i += 1
            if piece in MINISTER:
                if horizontal_displacement != 2:
                    raise ValueError("Invalid movement for minister. ")
                if d == "+":
                    i -= 2
                if d == "-":
                    i += 2
            if piece in KNIGHT:
                if horizontal_displacement not in (1, 2):
                    raise ValueError("Invalid movement for knight. ")
                if d == "+":
                    i -= 1 if horizontal_displacement == 2 else 2
                if d == "-":
                    i += 1 if horizontal_displacement == 2 else 2
        final = (i, j)

        return start[0] * 9 + start[1], final[0] * 9 + final[1]
