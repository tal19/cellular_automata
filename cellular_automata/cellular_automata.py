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
        that square is given.
    
    agent_positions : array
        The list of initial position tuples (column, row) for agents on plane.

    Attributes
    ----------
    agent_grid : array
        The grid of current positions of agents in plane.
    


    """

    def __init__(self, attribute_grid, agent_positions):
        self.type_grid = attribute_grid[:,:][0]
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
            self.decision_order[i] = np.argwhere(attribute_grid[:,:,0] == i)
        
    def move(self):
        for i in range(len(self.decision_order)):
            np.random.shuffle(self.decision_order[i])
            
            if i == 0:
                for j in self.decision_order:
                    #agent in exit position now leaves plane
                    if self.agent_grid[j[0], j[1]] == 1:
                        self.agent_grid[j[0], j[1]] = 0

                
            np.random.shuffle(self.decision_order[i])
            for j in self.decision_order:
                if j:
                    if self.agent_grid[j[0],j[1]] == 1:
                        if self.type_grid[j[0],j[1]] == 1: #if agent is currently in a seat
                            options = []
                            for k in [[0,1], [0,-1]]:
                                if (not self.type_grid[j[0] + k[0], j[1] + k[1]] == 2
                                    and self.agent_grid[j[0] + k[0], j[1] + k[1]] == 0 and 
                                    self.distance_grid[j[0] + k[0], j[1] + k[1]] <
                                    self.distance_grid[j[0],j[1]]):
                                    options.append(k) #append empty neighbouring seats with 
                                                    #a shorter distance to the exit
                            np.random.shuffle(options) #randomly choose one of equally good seats to move to
                            self.agent_grid[j[0] + options[0][0], j[1] + options[0][0]] == 1
                            self.agent_grid[j[0],j[1]] == 0
                        elif self.type_grid == 3: #if agent is currently in aisle
                            options = []
                            for k in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                                if (not self.type_grid[j[0] + k[0], j[1] + k[1]] == 2 and
                                    not self.type_grid[j[0] + k[0], j[1] + k[1]] == 1
                                    and self.agent_grid[j[0] + k[0], j[1] + k[1]] == 0 and 
                                    self.distance_grid[j[0] + k[0], j[1] + k[1]] <
                                    self.distance_grid[j[0],j[1]]):
                                    options.append(k) #append empty neighbouring seats with 
                                                    #a shorter distance to the exit
                            np.random.shuffle(options) #randomly choose one of equally good seats to move to
                            self.agent_grid[j[0] + options[0][0], j[1] + options[0][0]] == 1
                            self.agent_grid[j[0],j[1]] == 0

def visualise(Grid, t = "completion"):
    """Function to visualise the cellular automata evacuation model.

    Parameters
    ----------
    grid: Grid
        Initialised grid ready to have evacuation run on.
    
    t: Integer or "completion"
        Represents how many time steps to run model for.

        If t is integer run t times.

        If t = "completion", run until all agents have left plane.

    Return
    ----------
    Return visualisation of evacuation model simulation.

    """
    if isinstance(t, Number):
        for t in range(t):
            pyplot.clf()
            pyplot.matshow(grid.agent_grid, fignum=0, cmap='binary')
            pyplot.show()
            grid.move()
    else:
        while sum(sum(grid.agent_grid)) > 0:
            pyplot.clf()
            pyplot.matshow(grid.agent_grid, fignum=0, cmap='binary')
            pyplot.show()
            grid.move()
              




