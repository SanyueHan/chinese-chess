

BOUNDARY = {
    'r': lambda i, j: True,
    'k': lambda i, j: True,
    'c': lambda i, j: True,
    'm': lambda i, j: not (i in {3, 6} and j in {0, 2, 4, 6, 8}),
    'a': lambda i, j: i in {0, 1, 2, 7, 8, 9} and j in {3, 4, 5},
    'g': lambda i, j: i in {0, 1, 2, 7, 8, 9} and j in {3, 4, 5},
    'p': lambda i, j: True
}
