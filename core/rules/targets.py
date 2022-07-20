def rook_cannon_targets(tup):
    i, j = tup
    return [(i, j_) for j_ in range(9) if j_ != j] + [(i_, j) for i_ in range(10) if i_ != i]


def knight_targets(tup):
    i, j = tup
    return [(i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2), (i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1)]


def minister_targets(tup):
    i, j = tup
    return [(i + 2, j + 2), (i + 2, j - 2), (i - 2, j + 2), (i - 2, j - 2)]


def advisor_targets(tup):
    i, j = tup
    return [(i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]


def general_targets(tup):
    i, j = tup
    return [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]


TARGETS = {
    'r': rook_cannon_targets,
    'k': knight_targets,
    'c': rook_cannon_targets,
    'm': minister_targets,
    'a': advisor_targets,
    'g': general_targets,
}
