ENCODE = {
    '车': 'r',  # rook
    '马': 'k',  # knight
    '炮': 'c',  # cannon
    '相': 'm',  # minister
    '士': 'a',  # assistant
    '帅': 'g',  # general
    '兵': 'p',  # pawn
    '車': 'R',
    '馬': 'K',
    '砲': 'C',
    '象': 'M',
    '仕': 'A',
    '将': 'G',
    '卒': 'P',
}


DECODE = {e: c for c, e in ENCODE.items()}


def encode(string: str) -> str:
    return ''.join(ENCODE.get(c, ' ') for c in string)


def decode(string: str) -> str:
    return ''.join(DECODE.get(c, '\u3000') for c in string)
