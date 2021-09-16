from typing import List

from constants import DECODE, ENCODE
from core.board import *
from rules.boundaries import BOUNDARY
from rules.targets import TARGETS
from rules.paths import PATH


class State(Board):
    def __init__(self, board: Tuple[str], next_side: Role):
        super().__init__(board, next_side)
        self._valid_choices = {}

    def parse(self, command):
        """
        Input command, return start coordinate and final coordinate for the movement.
        Check whether the movement is allowed for that kind of piece only,
        without considering the restriction because of the other pieces on the board.
        Raise error if check failed.
        """
        movement = ''.join(ENCODE.get(c, c) for c in command)
        for c in movement:
            if self.next_side.OPPONENT.func(c):
                raise ValueError(f"{DECODE[c]} doesn't belongs to you. ")

        # get start coordinate
        if (piece := movement[0]) in PIECES and (position := movement[1]) in "123456789":
            p = int(position)
            if (n := self.cols[-p].count(piece)) != 1:
                if n == 0:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"no {DECODE[piece]} in column {p}")
                if n > 1:
                    raise ValueError(f"Invalid command: {''.join(DECODE[c] for c in movement)}, "
                                     f"multiple {DECODE[piece]} in column {p}")
            i = self.cols[-p].index(piece)
            j = self.N - p

        elif (piece := movement[1]) in PIECES and (position := movement[0]) in "^$":
            for j in range(self.N):
                col = self.cols[j]
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

        return start, final

    def is_valid(self, vector):
        """
        check whether the displacement is performable by ensuring that:
        1. the target is valid (not occupied by own pieces and not exceed bound)
        2. the path is valid (no obstacle for common pieces and one obstacle for cannon)
        If requirement is satisfied, produce the new board in tuple of string format
        """
        start, final = vector
        i_s, j_s = start
        i_f, j_f = final
        piece_s = self[i_s][j_s]
        if i_f < 0 or i_f > 9 or j_f < 0 or j_f > 8:
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} exceeds boundary. ")
        if not BOUNDARY[piece_s.lower()](i_f, j_f):
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} exceeds boundary. ")
        piece_f = self[i_f][j_f]

        side_s = State._get_side_for_piece(piece_s)
        side_f = State._get_side_for_piece(piece_f)
        if side_s == side_f:
            raise ValueError(f"Invalid movement, {DECODE[piece_s]} attacks friend. ")

        path = ''.join(self._occupation(point) for point in PATH[piece_s.lower()](vector))
        obstacle = len(path) - path.count(' ')
        if piece_s in CANNON and piece_f != ' ':
            # cannon is attacking, one obstacle should on the path
            if obstacle != 1:
                raise ValueError(f"Invalid path for {DECODE[piece_s]}. ")
        else:
            # cannon is not attacking or other pieces is moving or attacking, no obstacle should on the path
            if obstacle != 0:
                raise ValueError(f"Invalid path for {DECODE[piece_s]}. ")
        return vector

    def is_legal(self):
        """
        ensure the result will not:
        1. expose one general to the other
        2. enable the next player killing the other's general directly.
        """
        self_general = self._general_position(self._next_side)
        oppo_general = self._general_position(self._next_side.OPPONENT)
        if self_general[1] == oppo_general[1]:
            col = self.cols[self_general[1]]
            s = min(self_general[0], oppo_general[0])
            e = max(self_general[0], oppo_general[0])
            path = col[s + 1:e]
            if len(path) == path.count(' '):
                raise ValueError(f"Invalid movement: General exposed. ")
        for vector in self.valid_choices(self._next_side):
            if vector[1] == oppo_general:
                raise ValueError(f"Invalid movement: General will be killed. ")
        return self

    def valid_choices(self, side):
        if side not in self._valid_choices:
            self._valid_choices[side] = []
            vectors = sum(([(k, t) for t in self._targets(k, side)] for k in self.pieces(side)), [])
            for v in vectors:
                try:
                    self._valid_choices[side].append(self.is_valid(v))
                except ValueError:
                    pass
        return self._valid_choices[side]

    def _targets(self, tup, side) -> List[Tuple]:
        piece = self._occupation(tup)
        if fun := TARGETS.get(piece.lower()):
            return fun(tup)
        i, j = tup
        pawn_targets = []
        if self._general_position(side)[0] in (0, 1, 2):
            pawn_targets.append((i + 1, j))
            if i >= 5:
                pawn_targets.extend([(i, j + 1), (i, j - 1)])
        if self._general_position(side)[0] in (7, 8, 9):
            pawn_targets.append((i - 1, j))
            if i <= 4:
                pawn_targets.extend([(i, j + 1), (i, j - 1)])
        return pawn_targets
