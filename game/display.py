from enum import Enum
from functools import partial

from core.consts.coding import DECODE


class Fore(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    DARK_GREEN = 36
    WHITE = 37


class Back(Enum):
    BLACK = 40
    CRIMSON = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    DARK_GREEN = 46
    WHITE = 47


class Mode(Enum):
    DEFAULT = 0


def add_color(char, mode, fore, back):
    return f"\033[{mode.value};{fore.value};{back.value}m{char}\033[0m"


COLOR_WARM = partial(add_color, mode=Mode.DEFAULT, fore=Fore.BLACK, back=Back.WHITE)
COLOR_COOL = partial(add_color, mode=Mode.DEFAULT, fore=Fore.WHITE, back=Back.BLACK)


DISPLAY = {}


for k, v in DECODE.items():
    if k.islower():
        DISPLAY[k] = COLOR_WARM(v)
    if k.isupper():
        DISPLAY[k] = COLOR_COOL(v)


if __name__ == "__main__":
    for k, v in DISPLAY.items():
        print(k, v)
