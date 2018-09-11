import trie2

def get_valid_neighbors(puzzle, coord, visited):
    r_len = len(puzzle)
    c_len = len(puzzle[0])
    r_i = coord[0]
    c_i = coord[1]
    valid_neighbor_coords = []

    for r_n in range(r_i-1, r_i+2):
        for c_n in range(c_i-1, c_i+2):
            if (r_n >= 0) and (r_n < r_len):
                if (c_n >= 0) and (c_n < c_len):
                    if (r_n, c_n) not in visited:
                        valid_neighbor_coords.append((r_n, c_n))
    return valid_neighbor_coords


def _search(puzzle, dict, coord, prefix, visited):
    r_i = coord[0]
    c_i = coord[1]
    visited.add(coord)
    prefix += puzzle[r_i][c_i]
    words = []
    if dict.find(prefix):
        words.append(prefix)
    if dict.is_prefix(prefix):
        for neighbor in get_valid_neighbors(puzzle, coord, visited):
            words += _search(puzzle, dict, neighbor, prefix, visited.copy())
    return words

def search(puzzle, dict):
    words = []
    for r_i in range(len(puzzle)):
        for c_i in range(len(puzzle[0])):
            words += _search(puzzle, dict, (r_i, c_i), '', set())
    return words

PUZZLE = [['A','B','C','D','E'],
          ['F','P','G','H','I'],
          ['J','K','P','L','M'],
          ['N','O','P','L','Q'],
          ['R','S','T','U','E']]

trie = trie2.Trie()
trie.insert("ABC")
trie.insert("APPLE")
trie.insert("AFJ")
trie.insert("BCD")
trie.insert("CBA")
trie.insert("LLM")
print(search(PUZZLE, trie))
