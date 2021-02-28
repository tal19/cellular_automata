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

    def 
