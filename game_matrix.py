import Cell
import settings
game_matrix:list[list[Cell.Cell]] = [[Cell.Cell(i, j, "UNOCCUPIED") for i in range(settings.hor_cells)] for j in range(
    settings.ver_cells)]


'''
    ALL STATES:
        UNOCCUPIED - 0, 0, 0
        TERRAIN - 128, 128, 128
        CAPITAL - 115, 28, 178
        SUPPLY - 255, 206, 27
        COMBATANT - 255, 75, 75, 0
'''

state_colors = {
    "UNOCCUPIED" : (0, 0, 0),
    "TERRAIN": (128, 128, 128),
    "CAPITAL": (115, 28, 178),
    "SUPPLY": (255, 75, 75),
    "COMBATANT": (255, 206, 27)
}


next_state:dict[Cell.Cell,str] = dict()

def local_rule(cell: Cell.Cell, neighbors_list:list[Cell.Cell]):

    # neighbors_faction = "None"
    # for i in neighbors_list:
    #     if i.get_faction() != "None":
    #         neighbors_faction = i.get_faction()
    #         break

    neighbor_states = {
        "UNOCCUPIED" : 0,
        "TERRAIN": 0,
        "CAPITAL": 0,
        "SUPPLY": 0,
        "COMBATANT": 0
    }

    factions = {
        "X" : 0,
        "O" : 0,
        "None" : 0
    }

    anti = {"X" : "O", "O" : "X", "None" : "None"}

    for n in neighbors_list:
        neighbor_states[n.get_state()] += 1

    for n in neighbors_list:
        factions[n.get_faction()] += 1

    def decide_faction():
        if factions["X"] > factions["O"]:
            cell.set_faction("X")
        elif factions["O"] > factions["X"]:
            cell.set_faction("O")
        else:
            cell.set_faction("None")


    if cell.state == "CAPITAL":
        if neighbor_states["COMBATANT"] >= 1:
            if factions[anti[cell.get_faction()]] >= 1:
                next_state[cell] = "UNOCCUPIED"
                cell.set_faction("None")
                return

    elif cell.state == "UNOCCUPIED":
        if neighbor_states["CAPITAL"] > 3:
            next_state[cell] = "COMBATANT"
            decide_faction()
            return
        elif neighbor_states["COMBATANT"] > 1:
            next_state[cell] = "COMBATANT"
            decide_faction()
            return

    elif cell.state == "SUPPLY":
        if neighbor_states["COMBATANT"] > 1 and factions[anti[cell.get_faction()]]:
            next_state[cell] = "UNOCCUPIED"
            cell.set_faction("None")
            return
        elif neighbor_states["SUPPLY"] <= 1:
            next_state[cell] = "UNOCCUPIED"
            cell.set_faction("None")
            return


    elif cell.state == "COMBATANT":
        if neighbor_states["COMBATANT"] > 3 and factions[anti[cell.get_faction()]] < 1:
            next_state[cell] = "SUPPLY"
            decide_faction()
            return

        elif neighbor_states["SUPPLY"] < 1:
            next_state[cell] = "UNOCCUPIED"
            cell.set_faction("None")
            return

def sim():
    next_state.clear()
    for row in game_matrix:
        for cell in row:
            local_rule(cell, Cell.get_all_neighbors(cell))
    for k, v in next_state.items():
        k.set_state(v)