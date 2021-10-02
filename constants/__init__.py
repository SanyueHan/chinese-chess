import os
from enum import Enum

from .boards import OFFENSIVE_INIT, DEFENSIVE_INIT
from .color import COLOR_WARM, COLOR_COOL
from .coding import ENCODE, DECODE
from .help import HELP


class Role(Enum):
    OFFENSIVE = OFFENSIVE_INIT, str.islower
    DEFENSIVE = DEFENSIVE_INIT, str.isupper

    def __init__(self, init, func):
        self._init = init
        self._func = func

    def __repr__(self):
        return self.__str__()

    @property
    def init(self):
        return self._init

    @property
    def func(self):
        return self._func


Role.OFFENSIVE.OPPONENT = Role.DEFENSIVE
Role.DEFENSIVE.OPPONENT = Role.OFFENSIVE


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
