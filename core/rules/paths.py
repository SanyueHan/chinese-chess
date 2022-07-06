

def straight_path(vector):
    s, f = vector
    i_s, j_s = s
    i_f, j_f = f
    if i_s - i_f:
        return [(i, j_s) for i in range(min(i_s, i_f) + 1, max(i_s, i_f))]
    if j_s - j_f:
        return [(i_s, j) for j in range(min(j_s, j_f) + 1, max(j_s, j_f))]


def knight_path(vector):
    s, f = vector
    i_s, j_s = s
    i_f, j_f = f
    if abs(i_s - i_f) == 2:
        return [((i_s+i_f)//2, j_s)]
    if abs(j_s - j_f) == 2:
        return [(i_s, (j_s+j_f)//2)]


def minister_path(vector):
    s, f = vector
    i_s, j_s = s
    i_f, j_f = f
    return [((i_s+i_f)//2, (j_s+j_f)//2)]


PATH = {
    'r': straight_path,
    'k': knight_path,
    'c': straight_path,
    'm': minister_path,
    'a': lambda v: [],
    'g': straight_path,
    'p': lambda v: [],
}
