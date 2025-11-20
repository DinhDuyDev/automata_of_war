class Cell:
    all_cells = dict()
    id = 0

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.all_neighbors = [
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)
        ]
        self.id = Cell.id
        self.state = state

        self.faction = "None"

        self.strength = 25

        Cell.all_cells[(x, y)] = self
        Cell.id += 1

    def set_state(self, status : str):
        self.state = status

    def get_state(self):
        return self.state

    def get_faction(self):
        return self.faction

    def set_faction(self, faction):
        self.faction = faction

    def set_strength(self, strength):
        self.strength = strength

def get_all_neighbors(cell:Cell):
    x = cell.x
    y = cell.y
    all_neighbors = [
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    ]
    n = []
    for (x, y) in all_neighbors:
        if (x, y) in Cell.all_cells:
            n.append(Cell.all_cells[(x, y)])
    return n
