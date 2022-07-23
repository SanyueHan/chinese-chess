

def straight_path(vector):
    s, f = vector
    if s % 9 == f % 9:
        return range(min(s, f) + 9, max(s, f), 9)
    if s // 9 == f // 9:
        return range(min(s, f) + 1, max(s, f))


def knight_path(vector):
    s, f = vector
    i_s, j_s = s // 9, s % 9
    i_f, j_f = f // 9, f % 9
    if abs(i_s - i_f) == 2:
        return [(i_s + i_f) // 2 * 9 + j_s]
    if abs(j_s - j_f) == 2:
        return [i_s * 9 + (j_s + j_f) // 2]


def minister_path(vector):
    s, f = vector
    return [(s + f) // 2]


def vacant_path(vector):
    return []


PATH = {
    'r': straight_path,
    'k': knight_path,
    'c': straight_path,
    'm': minister_path,
    'a': vacant_path,
    'g': straight_path,
    'p': vacant_path,
}
