#include <ctype.h>
#include <stdlib.h>


int PALACE[90] = {
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0,
};

int EE[90] = {
        0, 0, 1, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 1, 0, 0,
        0, 0, 1, 0, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 1, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 1, 0, 0,
};


int in_boundary(int piece, int target)
{
    int res;
    switch (piece) {
        case 'A':
            res = PALACE[target];
            break;
        case 'G':
            res = PALACE[target];
            break;
        case 'M':
            res = EE[target];
            break;
        default:
            res = 1;
    }
    return res;
}

int role(char p)
{
    if (islower(p)) {
        return 1;
    } else if (isupper(p)) {
        return -1;
    } else {
        return 0;
    }
}

int number_of_obstacle_on_straight_path(char* board, int source, int target)
{
    int res = 0;
    int s;
    int e;
    int step;
    if (target > source) {
        s = source;
        e = target;
    } else if (source > target) {
        s = target;
        e = source;
    } else {
        return -1;
    }
    if (source % 9 == target % 9) {
        step = 9;
    } else if (source / 9 == target / 9) {
        step = 1;
    } else {
        return -1;
    }
    for (int i=s+step; i<e; i+=step) {
        if (isalpha(board[i])) {
            res += 1;
        }
    }
    return res;
}

int number_of_obstacle_on_minister_path(char* board, int source, int target)
{
    if (isalpha(board[(source + target) / 2])) {
        return 1;
    } else {
        return 0;
    }
}

int number_of_obstacle_on_knight_path(char* board, int source, int target)
{
    int source_i = source / 9;
    int source_j = source % 9;
    int target_i = target / 9;
    int target_j = target % 9;
    if (abs(source_i - target_i) == 2) {
        if (isalpha(board[(source_i+target_i)*9/2 + source_j])) {
            return 1;
        } else {
            return 0;
        }
    }
    if (abs(source_j - target_j) == 2) {
        if (isalpha(board[(source_j+target_j)/2 + source_i*9])) {
            return 1;
        } else {
            return 0;
        }
    }
    return -1;
}

int number_of_obstacle_on_path(char* board, int source, int target)
{
    int piece = toupper(board[source]);
    if (piece == 'R' || piece == 'C' || piece == 'G') {
        return number_of_obstacle_on_straight_path(board, source, target);
    } else if (piece == 'M') {
        return number_of_obstacle_on_minister_path(board, source, target);
    } else if (piece == 'K') {
        return number_of_obstacle_on_knight_path(board, source, target);
    } else {
        return 0;
    }
}


int is_valid(char* board, int source, int target)
{
    if (source < 0 || source > 89 || target < 0 || target > 89) {
        // exceed board
        return 0;
    }
    char piece_s = board[source];
    if (!in_boundary(toupper(piece_s), target)) {
        // exceed boundary
        return 0;
    }
    char piece_t = board[target];
    if (role(piece_t) == role(piece_s)) {
        // attacking friend
        return 0;
    }
    int n = number_of_obstacle_on_path(board, source, target);
    if (toupper(piece_s) == 'C' && isalpha(piece_t)) {
        // cannon is attacking, one obstacle should on the path
        return n == 1;
    } else {
        // otherwise, no obstacle should on the path
        return n == 0;
    }
}
