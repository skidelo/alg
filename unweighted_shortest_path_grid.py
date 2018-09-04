from maze import Box
import queue


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
            elif boxes[r_num][c_num].blocked:
                print("  X ", end='') if col.is_open("west") else print("| X ", end='')
            else:
                print("    ", end='') if col.is_open("west") else print("|   ", end='')
            if c_num == (len(row)-1):
                print("") if col.is_open("east") else print("|")

        # Print bottom
        if r_num == (len(boxes)-1):
            for col in row:
                print("+   ", end='') if col.is_open("south") else print("+---", end='')
            print("+")

def mark_and_add_neighbors(location, distances, grid, cur_distance, q):
    r, c = location[0], location[1]
    up = (r-1,c) if r-1 >= 0 else None
    right = (r,c+1) if c+1 < GRID_SIZE else None
    down = (r+1,c) if r+1 < GRID_SIZE else None
    left = (r,c-1) if c-1 >=0 else None

    for neighbor in (up, right, down, left):
        if neighbor is not None:
            n_r, n_c = neighbor
            if distances[n_r][n_c] == -1 and not grid[n_r][n_c].blocked:
                distances[n_r][n_c] = cur_distance+1
                q.put(neighbor)

def get_closer_neighbor(location, distances):
    r, c = location[0], location[1]
    l_distance = distances[location[0]][location[1]]
    up = (r-1,c) if r-1 >= 0 else None
    right = (r,c+1) if c+1 < GRID_SIZE else None
    down = (r+1,c) if r+1 < GRID_SIZE else None
    left = (r,c-1) if c-1 >=0 else None

    closer_neighbor = None
    for neighbor in (up, right, down, left):
        if neighbor is not None:
            if distances[neighbor[0]][neighbor[1]] == l_distance-1:
                closer_neighbor = neighbor
                break

    assert(closer_neighbor is not None)
    return closer_neighbor


def find_shortest_path(start, end, grid):
    distances = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    cur_distance = 0
    distances[start[0]][start[1]] = 0

    q = queue.Queue()
    location = start
    mark_and_add_neighbors(location, distances, grid, cur_distance, q)

    while not q.empty():
        location = q.get()
        cur_distance = distances[location[0]][location[1]]
        mark_and_add_neighbors(location, distances, grid, cur_distance, q)
        if location == end:
            break

    shortest_path = []
    if distances[end[0]][end[1]] != -1:
        shortest_path.append(end)
        closer_neighbor = get_closer_neighbor(end, distances)
        shortest_path.append(closer_neighbor)
        while closer_neighbor != start:
            closer_neighbor = get_closer_neighbor(closer_neighbor, distances)
            shortest_path.append(closer_neighbor)

    return shortest_path

if __name__ == '__main__':
    GRID_SIZE = 10

    grid = [[Box() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(1, GRID_SIZE):
        grid[GRID_SIZE-2][i].block()
    for i in range(1, GRID_SIZE-2):
        grid[i][2].block()
    for i in range(0, GRID_SIZE-3):
        grid[i][GRID_SIZE//2].block()

    shortest_path = find_shortest_path((GRID_SIZE-1,GRID_SIZE-1), (0,GRID_SIZE-1), grid)
    for r,c in shortest_path:
        grid[r][c].mark()
    print_boxes(grid)
