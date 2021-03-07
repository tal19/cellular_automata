import numpy as np
from matplotlib import pyplot
from numbers import Number

class Grid:
    """Grid class that initialises the grid for cellular automata model.

    Parameters
    ----------
    attribute_grid : array
        The array same dimension as plane, with each space containing tuple
        giving details about different square attributes.

        In first tuple position, gives detail about square type:
        1 = seat
        2 = wall/toilet
        3 = aisle
        4 = exit

        In second position, integer denoting shortest distance to exit from
        that square is given, this is a hard coded input(for now).
    
    agent_positions : array
        The list of initial position tuples (column, row) for agents on plane.

    Attributes
    ----------
    agent_grid : array
        The grid of current positions of agents in plane.
    


    """

    def __init__(self, attribute_grid, agent_positions):
        self.type_grid = attribute_grid[:,:, 0]
        agent_grid = np.zeros(np.shape(attribute_grid[:,:,0]))
        for pos in agent_positions:
            if not attribute_grid[pos[0],pos[1]][0] == 2:
                agent_grid[pos[0],pos[1]] = 1
            else:
                raise ValueError(f"Grid position {pos} cannot contain agent.")
        self.agent_grid = agent_grid
        self.distance_grid = attribute_grid[:,:,1]
        self.decision_order = [None]*(np.amax(attribute_grid[:,:,1])+1)
        for i in range(np.amax(attribute_grid[:,:,1])+1):
            self.decision_order[i] = np.argwhere(attribute_grid[:,:,1] == i)
        
    def move(self):
        for i in range(len(self.decision_order)):
            np.random.shuffle(self.decision_order[i])
            
            if i == 0:
                for j in self.decision_order[i]:
                    #agent in exit position now leaves plane
                    if self.agent_grid[j[0], j[1]] == 1:
                        self.agent_grid[j[0], j[1]] = 0

            else:  
                
                for j in self.decision_order[i]:
                
                    if self.agent_grid[j[0],j[1]] == 1:
                        if self.type_grid[j[0],j[1]] == 1: #if agent is currently in a seat
                            options = []
                            for k in [[0,1], [0,-1]]:
                                if ((not self.type_grid[j[0] + k[0], j[1] + k[1]] == 2)
                                    and (self.agent_grid[j[0] + k[0], j[1] + k[1]] == 0) and 
                                    (self.distance_grid[j[0] + k[0], j[1] + k[1]] <
                                    self.distance_grid[j[0],j[1]])):
                                    options.append(k) #append empty neighbouring seats with 
                            if options:                         #a shorter distance to the exit
                                np.random.shuffle(options)
                                print(options) #randomly choose one of equally good seats to move to
                                print((j[0] + options[0][0] ,j[1] + options[0][1]))
                                self.agent_grid[j[0] + options[0][0], j[1] + options[0][1]] = 1
                                self.agent_grid[j[0],j[1]] = 0
                        elif self.type_grid[j[0],j[1]] == 3: #if agent is currently in aisle
                            options = []
                            for k in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                                if (not self.type_grid[j[0] + k[0], j[1] + k[1]] == 2 and
                                    not self.type_grid[j[0] + k[0], j[1] + k[1]] == 1
                                    and self.agent_grid[j[0] + k[0], j[1] + k[1]] == 0 and 
                                    self.distance_grid[j[0] + k[0], j[1] + k[1]] <
                                    self.distance_grid[j[0],j[1]]):
                                    options.append(k) #append empty neighbouring seats with 
                                                    #a shorter distance to the exit
                            if options:
                                np.random.shuffle(options) #randomly choose one of equally good seats to move to
                                self.agent_grid[j[0] + options[0][0], j[1] + options[0][1]] = 1
                                self.agent_grid[j[0],j[1]] = 0
    
    def choose_move(self, ):
        """Makes a step based on local costs.

        Takes a dictionary with at least an entry with key "this".
        Returns the best possible move. If multiple ones are available, pick one randomly.
        """

    def get_local(self, x, y, info):
        """Takes grid position (x,y) and returns neighbouring/local position information."""
        if info = "cost":
            local = dict(this=self.distance_grid[x][y])
            if x > 0:
                local["up"] = self.distance_grid[x-1][y]
            if self.distance_grid.shape[1] > y+1:
                local["right"] = self.distance_grid[x][y+1]
            if self.distance_grid.shape[0] > x+1:
                local["down"] = self.distance_grid[x+1][y]
            if y > 0:
                local["left"] = self.distance_grid[x][y-1]
            return local
        elif info = "type":
            local = dict(this=self.type_grid[x][y])
            if x > 0:
                local["up"] = self.type_grid[x-1][y]
            if self.type_grid.shape[1] > y+1:
                local["right"] = self.type_grid[x][y+1]
            if self.type_grid.shape[0] > x+1:
                local["down"] = self.type_grid[x+1][y]
            if y > 0:
                local["left"] = self.type_grid[x][y-1]
            return local
    
    def check_boundaries(local_layout):
        """Return accessible neighbours."""
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








import copy
import dataclasses
import enum
import numpy as np
import random
import time
from matplotlib import pyplot


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

def remove_from_exit(layout, occupancy):
    for i in range(layout.shape[0]):
        for j in range(layout.shape[1]):
            if layout[i][j] == Cell.EXIT:
                occupancy[i][j] = False

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
        #display_cellular_space(layout, occupancy)
    remove_from_exit(layout, occupancy)
    return occupancy