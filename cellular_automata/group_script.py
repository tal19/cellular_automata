import copy
import dataclasses
import enum
import numpy as np
import random
import time


# Makes a step based on local costs.
# Takes a dictionary with at least an entry with key "this".
# Returns the best possible move. If multiple ones are available, pick one randomly.
def choose_move(local_costs):
    local_costs = copy.copy(local_costs)    # avoid modification of parameter.
    eliminated = []                         # Collector.
    min_cost = local_costs["this"]
    for i in local_costs:
        if local_costs[i] < 0:              # Collect non-accessible cells.
            eliminated.append(i)
        elif local_costs[i] > min_cost:     # Collect cells that are farther away from the exit than the current cell.
            eliminated.append(i)
        else:
            min_cost = local_costs[i]       # Update the minimum local cost.
    for i in local_costs:
        if i in eliminated:                 # Skip cells that are already eliminated.
            continue
        elif local_costs[i] > min_cost:
            eliminated.append(i)
    for i in eliminated:                    # Eliminate all the neighbours collected, the remaining will be the best.
        local_costs.pop(i)
    return random.choice(list(local_costs))     # Return a random one of them.


# Check if the boundary of the cell itself and neighbours allows migration.
# Takes a dictionary with at least an entry with key "this".
# Returns a dictionary with the rest keys, and boolean values indicating whether that cell is accessible.
def check_boundaries(local_layout):
    accessible = copy.copy(local_layout["this"].value.on_exit)     # Initialise with the exit conditions.
    eliminate = []
    for neighbour in accessible:                                   # Check if the neighbouring cells allows entry.
        if neighbour not in local_layout:                          # Pop if no actual neighbour.
            eliminate.append(neighbour)
        elif not local_layout[neighbour].value.on_entry[opposite(neighbour)]:   # Mark inaccessible on entry.
            accessible[neighbour] = False
    for e in eliminate:
        accessible.pop(e)
    return accessible


# Check if the neighbouring cells are vacant.
# Takes a dictionary with at least an entry with key "this".
# Returns a dictionary with the rest keys, and boolean values indicating whether that cell is empty.
def check_vacancies(local_occupancy):
    local_occupancy = copy.copy(local_occupancy)    # Avoid manipulating the original dictionary.
    local_occupancy.pop("this")
    for i in local_occupancy:
        local_occupancy[i] = not local_occupancy[i]
    return local_occupancy


# Return the opposite direction.
def opposite(direction):
    opp = None
    if direction == "up":
        opp = "down"
    elif direction == "right":
        opp = "left"
    elif direction == "down":
        opp = "up"
    elif direction == "left":
        opp = "right"
    return opp


# Return the local cells, i.e. this + neighbour.
# Takes a matrix as input and a pair of coordinates for location.
# Returns a dictionary with the names of the local cells and their values.
def get_local(matrix, x, y):
    local = dict(this=matrix[x][y])
    if x > 0:
        local["up"] = matrix[x-1][y]
    if matrix.shape[1] > y+1:
        local["right"] = matrix[x][y+1]
    if matrix.shape[0] > x+1:
        local["down"] = matrix[x+1][y]
    if y > 0:
        local["left"] = matrix[x][y-1]
    return local


# Move an agent towards a given direction in the occupancy matrix.
# Takes the occupancy matrix as input and a the agent's coordination, and the target direction.
# Returns the modified matrix (also modifies the input.
def move(occupancy, x, y, direction):
    if direction == "this":
        pass
    else:
        occupancy[x][y] = False
        if direction == "up":
            occupancy[x - 1][y] = True
        elif direction == "right":
            occupancy[x][y + 1] = True
        elif direction == "down":
            occupancy[x + 1][y] = True
        elif direction == "left":
            occupancy[x][y - 1] = True
    return occupancy


# Progress the simulation by one time step.
# Takes all three layers as input.
# Only modifies the the occupancy layer.
def make_step(layout, cost, occupancy):
    agents = np.transpose(np.random.permutation(np.argwhere(occupancy)))
    for i in range(agents.shape[1]):    # Cycle through each agents.
        x = agents[0][i]
        y = agents[1][i]                # Obtain the coordinates.
        local_cost = get_local(cost, x, y)  # Obtain the raw local cost.
        accessible = check_boundaries(get_local(layout, x, y))
        for j in accessible:
            if not accessible[j] and local_cost[j] >= 0:
                local_cost[j] = -2      # Mark as inaccessible by boundaries.
        vacant = check_vacancies(get_local(occupancy, x, y))
        for j in vacant:
            if (not vacant[j]) and local_cost[j] >= 0:
                local_cost[j] = -3      # Mark as inaccessible by occupancy.
        move(occupancy, x, y, choose_move(local_cost))
        display_cellular_space(layout, occupancy)
    return occupancy


# A shitty graphics output
# TODO: replace this piece of garbage.
def display_cellular_space(layout, occupancy):
    line = ""
    line += "╔"
    for j in range(layout.shape[1]):
        line += "═"
    line += "╗"
    print(line)
    for i in range(layout.shape[0]):
        line = ""
        line += "║"
        for j in range(layout.shape[1]):
            if layout[i][j].name == "WALL":
                line += "█"
            elif occupancy[i][j]:
                line += "*"
            elif layout[i][j].name == "SEAT":
                line += "_"
            elif layout[i][j].name == "FLOOR":
                line += " "
            elif layout[i][j].name == "EXIT":
                line += "×"
        line += "║"
        print(line)
    line = ""
    line += "╚"
    for j in range(layout.shape[1]):
        line += "═"
    line += "╝"
    print(line)
    time.sleep(0.1)


# A dataclass that collects the boundary conditions.
@dataclasses.dataclass
class Boundaries:
    on_entry:   dict[bool]
    on_exit:    dict[bool]


# An enumeration that collects all the boundary conditions.
class Cell(enum.Enum):
    WALL = Boundaries(on_entry=dict(up=False, right=False, down=False, left=False),
                      on_exit=dict(up=False, right=False, down=False, left=False))
    FLOOR = Boundaries(on_entry=dict(up=True, right=True, down=True, left=True),
                       on_exit=dict(up=True, right=True, down=True, left=True))
    SEAT = Boundaries(on_entry=dict(up=True, right=True, down=False, left=True),
                      on_exit=dict(up=True, right=True, down=False, left=True))
    EXIT = Boundaries(on_entry=dict(up=True, right=True, down=True, left=True),
                      on_exit=dict(up=False, right=False, down=False, left=False))


# Tests
# Test data
c = np.array([[-1, 15, 14, 13, 12, 13, 14, 15, -1],
              [-1, 14, 13, 12, 11, 12, 13, 14, -1],
              [-1, 13, 12, 11, 10, 11, 12, 13, -1],
              [-1, 12, 11, 10,  9, 10, 11, 12, -1],
              [-1, 11, 10,  9,  8,  9, 10, 11, -1],
              [-1, 10,  9,  8,  7,  8,  9, 10, -1],
              [-1, -1, -1, -1,  6, -1, -1, -1, -1],
              [-1, -1, -1, -1,  5, -1, -1, -1, -1],
              [ 0,  1,  2,  3,  4,  3,  2,  1,  0]])
o = np.array([[False, True, True, True, False, True, True, True, False],
              [False, True, True, True, False, True, True, True, False],
              [False, True, True, True, False, True, True, True, False],
              [False, True, True, True, False, True, True, True, False],
              [False, True, True, True, False, True, True, True, False],
              [False, True, True, True, False, True, True, True, False],
              [False, False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False, False]])
l = np.array([[Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.FLOOR, Cell.SEAT, Cell.SEAT, Cell.SEAT, Cell.WALL],
              [Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL, Cell.FLOOR, Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL],
              [Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL, Cell.FLOOR, Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL],
              [Cell.EXIT, Cell.FLOOR, Cell.FLOOR, Cell.FLOOR, Cell.FLOOR, Cell.FLOOR, Cell.FLOOR, Cell.FLOOR, Cell.EXIT]])
l_c = {"this": 10, "up": 11, "right": 9, "down": 9, "left": 11}
l_c_t = {"this": Cell.SEAT, "up": Cell.SEAT, "right": Cell.SEAT,
         "down": Cell.SEAT, "left": Cell.SEAT}
l_o = {"this": True, "up": True, "right": False, "down": False, "left": False}
# Test lines
while True:
    o = np.array([[False, True, True, True, False, True, True, True, False],
                  [False, True, True, True, False, True, True, True, False],
                  [False, True, True, True, False, True, True, True, False],
                  [False, True, True, True, False, True, True, True, False],
                  [False, True, True, True, False, True, True, True, False],
                  [False, True, True, True, False, True, True, True, False],
                  [False, False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False, False],
                  [False, False, False, False, False, False, False, False, False]])
    display_cellular_space(l, o)
    make_step(l, c, o)