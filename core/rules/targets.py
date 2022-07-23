KNIGHT_POSSIBLE_MOVEMENT = (9 + 2, 9 - 2, -9 + 2, -9 - 2, 18 + 1, 18 - 1, -18 + 1, -18 - 1)


KNIGHT_TARGETS_TABLE = (
    0b10001000, 0b10001100, 0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b11001100, 0b01001100, 0b01000100,
    0b10101000, 0b10101100, 0b11111100, 0b11111100, 0b11111100, 0b11111100, 0b11111100, 0b01011100, 0b01010100,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10101010, 0b10101111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b01011111, 0b01010101,
    0b10100010, 0b10100011, 0b11110011, 0b11110011, 0b11110011, 0b11110011, 0b11110011, 0b01010011, 0b01010001,
    0b00100010, 0b00100011, 0b00110011, 0b00110011, 0b00110011, 0b00110011, 0b00110011, 0b00010011, 0b00010001,
)


KNIGHT_TARGET_CACHE = []


for source_, targets in enumerate(KNIGHT_TARGETS_TABLE):
    targets_list = []
    for index_, displacement in enumerate(KNIGHT_POSSIBLE_MOVEMENT):
        if targets & (0b10000000 >> index_):
            targets_list.append(source_ + displacement)
    KNIGHT_TARGET_CACHE.append(targets_list)


def rook_cannon_targets(source):
    i, j = source // 9, source % 9
    return [i * 9 + j_ for j_ in range(9) if j_ != j] + [i_ * 9 + j for i_ in range(10) if i_ != i]


def knight_targets(source):
    """
    can't just return
    [source + 11, source + 7, source - 7, source - 11, source + 19, source + 17, source - 17, source - 19]
    because 81 + 7 = 89 is actually a wrong knight movement.
    """
    return KNIGHT_TARGET_CACHE[source]


def minister_targets(source):
    return [source + 20, source + 16, source - 16, source - 20]


def advisor_targets(source):
    return [source + 10, source + 8, source - 8, source - 10]


TARGETS = {
    'r': rook_cannon_targets,
    'k': knight_targets,
    'c': rook_cannon_targets,
    'm': minister_targets,
    'a': advisor_targets,
}
