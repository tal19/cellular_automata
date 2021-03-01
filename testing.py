from cellular_automata.cellular_automata import Grid, visualise
import numpy as np
atts = np.array([[(2, 0), (2, 0), (2, 0), (2, 0), (2, 0)], [(2, 0), (1, 5), (3, 4), (1, 5), (2, 0)], [(2, 0),(2, 0),(3, 3), (2, 0), (2, 0)], [(4, 0), (3, 1), (3, 2), (3, 1), (4, 0)], [(2, 0), (2, 0), (2, 0), (2, 0), (2, 0)]])
agent_list = [(1,1)]
grid = Grid(atts, agent_list)
grid.move()
