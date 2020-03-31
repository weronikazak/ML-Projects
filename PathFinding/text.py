class Tile():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def find_path(MAZE, START, END):
    start_tile = Tile(None, START)
    start_tile.g = start_tile.f = start_tile.h = 0
    end_tile = Tile(None, END)
    end_tile.f = end_tile.h = end_tile.g = 0

    o_list, c_list = [], []

    o_list.append(start_tile)

    while len(o_list) > 0:
        tile = o_list[0]
        tile_id = 0
        for i, item in enumerate(o_list):
            if item.f < tile.f:
                tile = item
                tile_id = i
        
        o_list.pop(tile_id)
        c_list.append(tile)

        if tile == end_tile:
            path = []
            current = tile
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for pos in ADJACENTS:
            tile_pos = (tile.position[0] + pos[0], tile.position[1] + pos[1])

            if (tile_pos[0] > 9
            # (len(MAZE) - 1)
                or tile_pos[0] < 0
                or tile_pos[1] > 9 
                # (len(MAZE[len(MAZE) - 1])-1)
                or tile_pos[1] < 0):
                continue

            if MAZE[tile_pos[0]][tile_pos[1]] != 0:
                continue

            new_tile = Tile(tile, tile_pos)

            children.append(new_tile)


        for child in children:
            for c in c_list:
                if child == c:
                    break
            else:
                child.g = tile.g + 1
                child.h = abs(child.position[0] - end_tile.position[0]) + abs(child.position[1] - end_tile.position[1])
                child.f = child.g + child.h

                for o in o_list:
                    if child == o and child.g >= o.g:
                        break
                else:
                    o_list.append(child)




MAZE = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

WIDTH, HEIGHT = 10, 10

ADJACENTS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

START = (0, 0)
END = (0, 9)

PATH = find_path(MAZE, START, END)

for x in range(WIDTH):
    line = ""
    for y in range(HEIGHT):
        i = MAZE[x][y]
        i = str(i)
        if i=="0": i = "_"
        elif i=="1": i = "#"

        if (x, y) in PATH:
            i = "A"
        line += i + " "
    print(line)