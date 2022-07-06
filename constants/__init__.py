import os
from enum import Enum

from .boards import BOARDS
from .color import COLOR_WARM, COLOR_COOL
from .coding import ENCODE, DECODE
from .help import HELP


class Role(Enum):
    OFFENSIVE = str.islower, None
    DEFENSIVE = str.isupper, None

    def __init__(self, iff_func, opponent):
        """
        :param iff_func: IFF (Identification Friend or Foe) function
        :param opponent:
        """
        self._iff_func = iff_func
        self._opponent = opponent

    def __repr__(self):
        return self.__str__()

    @property
    def iff_func(self):
        """
        :return: the function that returns True for self pieces and False for enemy pieces
        """
        return self._iff_func

    @property
    def opponent(self) -> 'Role':
        return self._opponent


Role.OFFENSIVE._opponent = Role.DEFENSIVE
Role.DEFENSIVE._opponent = Role.OFFENSIVE


TURN = {
    0: Role.OFFENSIVE,
    1: Role.DEFENSIVE
}


DISPLAY = {
    ' ': '\u3000'
}


for k, v in DECODE.items():
    if k.islower():
        DISPLAY[k] = COLOR_WARM(v)
    else:
        DISPLAY[k] = COLOR_COOL(v)


SIDE = {}
for k in DECODE:
    if k.isalpha() and k.islower():
        SIDE[k] = Role.OFFENSIVE
    if k.isalpha() and k.isupper():
        SIDE[k] = Role.DEFENSIVE


DEVELOPER_MODE = bool(os.environ.get("DEV_MODE"))


if __name__ == "__main__":
    print(Role.OFFENSIVE.opponent)
    print(Role.DEFENSIVE.opponent)
