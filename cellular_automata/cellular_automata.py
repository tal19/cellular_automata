import numpy as np

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
        agent_grid = np.zeros(np.shape(attribute_grid))
        for pos in agent_positions:
            if not attribute_grid[pos[0],pos[1]] == 2:
                agent_grid[pos[0],pos[1]] = 1
            else:
                raise ValueError(f"Grid position {pos} cannot contain agent.")
        self.agent_grid = agent_grid
        self.distance_grid = attribute_grid[:,:][1]
        self.decision_order = [None]*(max(attribute_grid[:,:][1])+1)
        for i in range(max(attribute_grid[:,:][1])+1):
            self.decision_order[i] = np.argwhere(a[:,:,0] == i)
        
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
                if self.agent_grid[j[0],j[1]] == 1:
                    if self.type_grid[j[0],j[1]] == 1: #if agent is currently in a seat
                        options = []
                        for k in [[0,1], [0,-1]]:
                            if (not self.attribute_grid[j[0] + k[0], j[1] + k[1]] == 2
                                and self.agent_grid[j[0] + k[0], j[1] + k[1]] == 0 and 
                                self.distance_grid[j[0] + k[0], j[1] + k[1]] <
                                self.distance_grid[j[0],j[1]]):
                                options.append(k) #append empty neighbouring seats with 
                                                  #a shorter distance to the exit
                        np.random.shuffle(options)
                        self.agent_grid[j[0] + options[0][0], j[1] + options[0][0]] == 1
                        self.agent_grid[j[0],j[1]] == 0

                    elif self.type_grid == 3: #if agent is currently in aisle
                    




