import random
import sys
sys.setrecursionlimit(10000) # 10000 is an example, try with different values

class Box(object):
    def __init__(self):
        self.openings = {
            "north": False,
            "east" : False,
            "south": False,
            "west": False
        }
        self._marked = False

    def open_side(self, side):
        self.openings[side] = True

    def is_open(self, side):
        return self.openings[side]

    def mark(self):
        self._marked = True

    def unmark(self):
        self._marked = False

    @property
    def marked(self):
        return self._marked


def print_boxes(boxes):
    # Print top
    for r_num, row in enumerate(boxes):
        for col in row:
            print("+   ", end='') if col.is_open("north") else print("+---", end='')
        print("+")

        # Print middle
        for c_num, col in enumerate(row):
            if boxes[r_num][c_num].marked:
                print("  * ", end='') if col.is_open("west") else print("| * ", end='')
            else:
                print("    ", end='') if col.is_open("west") else print("|   ", end='')
            if c_num == (len(row)-1):
                print("") if col.is_open("east") else print("|")

        # Print bottom
        if r_num == (len(boxes)-1):
            for col in row:
                print("+   ", end='') if col.is_open("south") else print("+---", end='')
            print("+")


def edge_index_to_box_index(boxes, edge_index):
    l_row = len(boxes)
    l_col = len(boxes[0])
    r = c = -1
    if edge_index in range(0, l_row):
        r = edge_index
        c = 0
    elif edge_index in range(l_row, l_row+l_col):
        r = l_row-1
        c = edge_index-l_col
    elif edge_index in range(l_row+l_col, 2*l_row+l_col):
        r = l_row-(edge_index-(l_row+l_col)+1)
        c = l_col-1
    elif edge_index in range(2*l_row+l_col, (2*l_row)+(2*l_col)):
        r = 0
        c = l_col-(edge_index-(2*l_row+l_col)+1)
    else:
        raise ValueError("Invalid edge index {})".format(edge_index))
    return r, c


def make_maze(boxes):
    l_row = len(boxes)
    l_col = len(boxes[0])
    entry = random.randrange(2*l_row+2*l_col)
    exit = entry
    while exit == entry:
        entry = random.randrange(2*l_row+2*l_col)

    for x in (entry, exit):
        if x in range(0, l_row):
            boxes[x][0].open_side("west")
        elif x in range(l_row, l_row+l_col):
            boxes[l_row-1][x-l_col].open_side("south")
        elif x in range(l_row+l_col, 2*l_row+l_col):
            boxes[l_row-(x-(l_row+l_col)+1)][l_col-1].open_side("east")
        elif x in range(2*l_row+l_col, (2*l_row)+(2*l_col)):
            boxes[0][l_col-(x-(2*l_row+l_col)+1)].open_side("north")
        else:
            raise ValueError("Invalid entry/exit value ({}/{})".format(entry, exit))

    visited = set()
    r_start = random.randrange(l_row)
    c_start = random.randrange(l_col)
    carve_path(boxes, visited, r_start, c_start)
    return entry, exit


def get_unvisited_neighbors(boxes, visited, r, c):
    l_row = len(boxes)
    l_col = len(boxes[0])
    univisited_neighbors = []
    if r >= 1 and boxes[r-1][c] not in visited:
        univisited_neighbors.append((r-1, c))
    if r < l_row-1 and boxes[r+1][c] not in visited:
        univisited_neighbors.append((r+1, c))
    if c >= 1 and boxes[r][c-1] not in visited:
        univisited_neighbors.append((r, c-1))
    if c < l_col-1 and boxes[r][c+1] not in visited:
        univisited_neighbors.append((r, c+1))

    return univisited_neighbors

def get_neighbor_direction(r, c, neighbor_r, neighbor_c):
    direction = None
    if r-neighbor_r == 1 and c-neighbor_c == 0:
        direction = 'north'
    elif r-neighbor_r == -1 and c-neighbor_c == 0:
        direction = 'south'
    elif r-neighbor_r == 0 and c-neighbor_c == 1:
        direction = 'west'
    elif r-neighbor_r == 0 and c-neighbor_c == -1:
        direction = 'east'
    else:
        raise ValueError('Not a valid neighbor')
    return direction


def opposite(direction):
    opposite_dir = None
    if direction == 'north':
        opposite_dir = 'south'
    elif direction == 'south':
        opposite_dir = 'north'
    elif direction == 'east':
        opposite_dir = 'west'
    elif direction == 'west':
        opposite_dir = 'east'
    else:
        raise ValueError('Invalid direction provided')
    return opposite_dir

def at_open_edge(boxes, r, c):
    result = False
    r_len = len(boxes)
    c_len = len(boxes[0])
    # Corners
    if r == 0 and c == 0:
        result = boxes[r][c].is_open('north') or boxes[r][c].is_open('west')
    elif r == 0 and c == c_len-1:
        result = boxes[r][c].is_open('north') or boxes[r][c].is_open('east')
    elif r == r_len-1 and c == 0:
        result = boxes[r][c].is_open('west') or boxes[r][c].is_open('south')
    elif r == r_len-1 and c == c_len-1:
        result = boxes[r][c].is_open('east') or boxes[r][c].is_open('south')

    # Edges
    elif r == 0:
        result = boxes[r][c].is_open('north')
    elif r == r_len-1:
        result = boxes[r][c].is_open('south')
    elif c == 0:
        result = boxes[r][c].is_open('west')
    elif c == c_len-1:
        result = boxes[r][c].is_open('east')
    return result



def carve_path(boxes, visited, r, c):
    visited.add(boxes[r][c])
    while True:
        neighbors = get_unvisited_neighbors(boxes, visited, r, c)
        if not neighbors:
            break
        r_random_neighbor, c_random_neighbor = neighbors[random.randrange(len(neighbors))]
        neighbor_direction = get_neighbor_direction(r, c, r_random_neighbor, c_random_neighbor)
        boxes[r][c].open_side(neighbor_direction)
        boxes[r_random_neighbor][c_random_neighbor].open_side(opposite(neighbor_direction))
        carve_path(boxes, visited, r_random_neighbor, c_random_neighbor)

def get_open_unvisited_neighbors(boxes, visited, r, c):
    open_unvisited = []
    univisited_neighbors = get_unvisited_neighbors(boxes, visited, r, c)
    for n_r, n_c in univisited_neighbors:
        if boxes[r][c].is_open(get_neighbor_direction(r, c, n_r, n_c)):
            open_unvisited.append((n_r, n_c))
    return open_unvisited


def traverse(boxes, visited, r, c, path):
    path = path.copy()
    visited.add(boxes[r][c])
    path.append((r,c))
    solution = []
    if len(path) > 1 and at_open_edge(boxes, r, c):
        solution = path
    while len(solution) == 0:
        neighbors = get_open_unvisited_neighbors(boxes, visited, r, c)
        if not neighbors:
            break
        r_random_neighbor, c_random_neighbor = neighbors[random.randrange(len(neighbors))]
        solution = traverse(boxes, visited, r_random_neighbor, c_random_neighbor, path)
    return solution


def solve_maze(boxes, entry_edge_index):
    r, c = edge_index_to_box_index(boxes, entry_edge_index)
    visited = set()
    solution = traverse(boxes, visited, r, c, [])
    for r, c in solution:
        boxes[r][c].mark()
    return solution

NUM_ROWS = 10
NUM_COLUMNS = 10
boxes = [[Box() for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]
entry_edge_i, _ = make_maze(boxes)
# print_boxes(boxes) # Prints maze before solving
solution = solve_maze(boxes, entry_edge_i)
print_boxes(boxes)

# Calculate percentage of marked boxes (maze coverage)
marked = 0
for row in boxes:
    for col in row:
        if col.marked:
            marked += 1
print("Maze coverage: {0:g}%".format((float(marked)/(len(boxes)*len(boxes[0])))*100))
