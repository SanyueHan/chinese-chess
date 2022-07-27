import re

from core.consts.coding import ENCODE


PIECE = ''.join(ENCODE.keys())
NUMBER = "一二三四五六七八九"
CN2NUM = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
}


COMMAND_PATTERN_1 = re.compile(f"([{PIECE}][{NUMBER}])([平进退][{NUMBER}])")
COMMAND_PATTERN_2 = re.compile(f"([前后][{PIECE}])([平进退][{NUMBER}])")


if __name__ == "__main__":
    c1 = "马八进七"
    c2 = "前车进一"

    r1 = COMMAND_PATTERN_1.fullmatch(c1)
    print(r1.group(1), r1.group(2))

    r2 = COMMAND_PATTERN_2.fullmatch(c2)
    print(r2.group(1), r2.group(2))
