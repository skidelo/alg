import math
import copy

def has_duplicate(iterable):
    unique = set()
    if type(iterable[0]) is int:
        # 1-D List
        for x in iterable:
            if x in unique:
                return True
            if -1 != x:
                unique.add(x)
    else:
        # 2-D Grid
        for r in iterable:
            for c in r:
                if c in unique:
                    return True
                if -1 != c:
                    unique.add(c)
    return False

def get_sub_grid(puzzle, coord):
    r, c = coord[0], coord[1]
    grid_size = int(math.sqrt(len(puzzle)))
    smallest_c = (c // grid_size) * grid_size
    smallest_r = (r // grid_size) * grid_size
    largest_c = smallest_c + grid_size
    largest_r = smallest_r + grid_size
    sub_grid = [r[smallest_c:largest_c] for r in puzzle[smallest_r:largest_r]]
    return sub_grid


def is_valid(puzzle, coord):
    if not (coord and puzzle):
        return False
    r, c = coord[0], coord[1]
    if puzzle[r][c] == -1:
        return False
    row = puzzle[r]
    return not has_duplicate(row) and not has_duplicate([_row[c] for _row in puzzle]) and not has_duplicate(get_sub_grid(puzzle, coord))

def get_next_empty_coord(puzzle):
    for r_i, r in enumerate(puzzle):
        for c_i, c in enumerate(r):
            if c == -1:
                return (r_i, c_i)
    return None

def is_filled(puzzle):
    for r in puzzle:
        for c in r:
            if c == -1:
                return False
    return True

def solve_sudoku(puzzle, coord):
    if is_filled(puzzle) and not coord:
        return puzzle
    if coord and puzzle[coord[0]][coord[1]] != -1:
        return solve_sudoku(puzzle, get_next_empty_coord(puzzle))

    puzzle = copy.deepcopy(puzzle)
    r, c = coord[0], coord[1]
    to_attempt = [x for x in range(1, 10)]
    while len(to_attempt):
        puzzle[r][c] = to_attempt.pop()
        if is_valid(puzzle, coord):
            sub_puzzle = solve_sudoku(puzzle, get_next_empty_coord(puzzle))
            if sub_puzzle:
                return sub_puzzle
    return None

def print_sudoku(puzzle):
    for r_i, r in enumerate(puzzle):
        if r_i % 3 == 0:
            print('-------------------------')
        for c_i, c in enumerate(r):
            if c_i == 0 or c_i % 3 == 0:
                print('|', end=' ')
            print(c, end=' ')
            if c_i == 8:
                print('|')
        if r_i == 8:
            print('-------------------------')


PUZZLE = [[-1,-1,-1,2,6,-1,7,-1,1],
          [6,8,-1,-1,7,-1,-1,9,-1],
          [1,9,-1,-1,-1,4,5,-1,-1],
          [8,2,-1,1,-1,-1,-1,4,-1],
          [-1,-1,4,6,-1,2,9,-1,-1],
          [-1,5,-1,-1,-1,3,-1,2,8],
          [-1,-1,9,3,-1,-1,-1,7,4],
          [-1,4,-1,-1,5,-1,-1,3,6],
          [7,-1,3,-1,1,8,-1,-1,-1]]

answer = solve_sudoku(PUZZLE, (0, 0))
if answer:
    print_sudoku(answer)
else:
    print("No solution.")
