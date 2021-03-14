import copy
import dataclasses
import enum
import numpy as np
import random
from matplotlib import pyplot


class Grid:
    """Grid class to model evacuation using 3 grids."""

    def __init__(self, layout, distance_grid, agent_positions):
        """Initialise 3 arrays.

        Layout: array
        Containing cell types.

        Cost: array
        Containing shortest distance of each cell from the source.

        Occupancy: array
        Containing information about current occupancy of each grid space.
        """

        self.layout = layout  # initialise layout grid
        # agent_grid = np.zeros(np.shape(layout[:,:,0]))
        # for pos in agent_positions:
        #     if not layout[pos[0],pos[1]][0] == 2:
        #         agent_grid[pos[0],pos[1]] = 1
        #     else:
        #         raise ValueError(f"Grid position {pos}
        #                          cannot contain agent.")
        self.occupancy = agent_positions
        self.cost = distance_grid
        self.reaction_time = np.zeros(np.shape(layout))
        # add a random reaction time for each agent
        for i in range(np.shape(layout)[0]):
            for j in range(np.shape(layout)[1]):
                if self.occupancy[i][j]:
                    self.reaction_time[i][j] = abs(np.random.normal(
                        loc=13, scale=1.5)//1)
        self.leaving = 0

    def get_local_cost(self, x, y):
        """Return the local cells cost, i.e. this + neighbour.

        Returns a dictionary with the names of the local cells
        and their cost values.
        """

        local = dict(this=self.cost[x][y])
        if x > 0:
            local["up"] = self.cost[x-1][y]
        if self.cost.shape[1] > y+1:
            local["right"] = self.cost[x][y+1]
        if self.cost.shape[0] > x+1:
            local["down"] = self.cost[x+1][y]
        if y > 0:
            local["left"] = self.cost[x][y-1]
        return local

    def get_local_layout(self, x, y):
        """Return the local cells layout, i.e. this + neighbour.

        Returns a dictionary with the names of the local cells and
        their layout type.
        """

        local = dict(this=self.layout[x][y])
        if x > 0:
            local["up"] = self.layout[x-1][y]
        if self.layout.shape[1] > y+1:
            local["right"] = self.layout[x][y+1]
        if self.layout.shape[0] > x+1:
            local["down"] = self.layout[x+1][y]
        if y > 0:
            local["left"] = self.layout[x][y-1]
        return local

    def get_local_occupancy(self, x, y):
        """Return the local cells occupancy, i.e. this + neighbour.

        Returns a dictionary with the names of the local cells and their
        occupancy state.
        """

        local = dict(this=self.occupancy[x][y])
        if x > 0:
            local["up"] = self.occupancy[x-1][y]
        if self.occupancy.shape[1] > y+1:
            local["right"] = self.occupancy[x][y+1]
        if self.occupancy.shape[0] > x+1:
            local["down"] = self.occupancy[x+1][y]
        if y > 0:
            local["left"] = self.occupancy[x][y-1]
        return local

    def move(self, x, y, direction):
        """Move an agent towards a given direction in the occupancy matrix.

        Takes the occupancy matrix as input and a the agent's coordination,
        and the target direction.
        Returns the modified matrix (also modifies the input.
        """

        if direction == "this":
            pass
        else:
            self.occupancy[x][y] = False
            if direction == "up":
                self.occupancy[x - 1][y] = True
            elif direction == "right":
                self.occupancy[x][y + 1] = True
            elif direction == "down":
                self.occupancy[x + 1][y] = True
            elif direction == "left":
                self.occupancy[x][y - 1] = True

    def remove_from_exit(self):
        """Remove agent from occupancy once they have reached exit."""

        for i in range(self.layout.shape[0]):
            for j in range(self.layout.shape[1]):
                if self.layout[i][j] == Cell.EXIT:
                    self.leaving = 1  # slide in use
                    self.occupancy[i][j] = False

    def make_step(self):
        """Progress the simulation by one time step.

        Takes all three layers as input.
        Only modifies the the occupancy layer.
        """

        self.leaving = 0  # reset slide data
        agents = np.transpose(
            np.random.permutation(np.argwhere(self.occupancy))
            )  # randomly order agents
        for i in range(agents.shape[1]):    # Cycle through each agents
            if not self.reaction_time[agents[0][i], agents[1][i]]:
                x = agents[0][i]
                y = agents[1][i]                # Obtain the coordinates
                local_cost = self.get_local_cost(x, y)  # Obtain local cost
                accessible = check_boundaries(self.get_local_layout(x, y))
                for j in accessible:
                    if not accessible[j] and local_cost[j] >= 0:
                        local_cost[j] = -2      # Mark as inaccessible
                vacant = check_vacancies(self.get_local_occupancy(x, y))
                for j in vacant:
                    if (not vacant[j]) and local_cost[j] >= 0:
                        local_cost[j] = -3      # Mark as inaccessible
                self.move(x, y, choose_move(local_cost))
                # display_cellular_space(layout, occupancy)
            else:
                self.reaction_time[agents[0][i], agents[1][i]] -= 1
        self.remove_from_exit()


def choose_move(local_costs):
    """Makes a step based on local costs.

    Takes a dictionary with at least an entry with key "this".
    Returns the best possible move. If multiple ones are available,
    pick one randomly.
    """

    local_costs = copy.copy(local_costs)    # avoid modification of parameter
    eliminated = []                         # Collector
    min_cost = local_costs["this"]
    for i in local_costs:
        if local_costs[i] < 0:              # Collect non-accessible cells
            eliminated.append(i)
        elif local_costs[i] > min_cost:  # Collect cells farther away from exit
            eliminated.append(i)
        else:
            min_cost = local_costs[i]       # Update the minimum local cost.
    for i in local_costs:
        if i in eliminated:                 # Skip cells already eliminated.
            continue
        elif local_costs[i] > min_cost:
            eliminated.append(i)
    for i in eliminated:               # Eliminate all the neighbours collected
        local_costs.pop(i)
    return random.choice(list(local_costs))     # Return a random one of them.


def check_boundaries(local_layout):
    """Check if the boundary of the cell itself and neighbours allows migration.

    Takes a dictionary with at least an entry with key "this".
    Returns a dictionary with the rest keys, and boolean values indicating
    whether that cell is accessible.
    """

    # Initialise with the exit conditions.
    accessible = copy.copy(local_layout["this"].value.on_exit)
    eliminate = []
    for neighbour in accessible:  # Check if neighbouring cells allows entry
        if neighbour not in local_layout:  # Pop if no actual neighbour.
            eliminate.append(neighbour)
        elif not local_layout[neighbour].value.on_entry[opposite(neighbour)]:
            # Mark inaccessible on entry.
            accessible[neighbour] = False
    for e in eliminate:
        accessible.pop(e)
    return accessible


def check_vacancies(local_occupancy):
    """Check if the neighbouring cells are vacant.

    Takes a dictionary with at least an entry with key "this".
    Returns a dictionary with the rest keys, and boolean values
    indicating whether that cell is empty.
    """

    local_occupancy = copy.copy(local_occupancy)
    # Avoid manipulating the original dictionary.
    local_occupancy.pop("this")
    for i in local_occupancy:
        local_occupancy[i] = not local_occupancy[i]
    return local_occupancy


def opposite(direction):
    """Return the opposite direction."""

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


# A dataclass that collects the boundary conditions.
@dataclasses.dataclass
class Boundaries:
    on_entry:   dict[bool]
    on_exit:    dict[bool]


# An enumeration that collects all the boundary conditions.
class Cell(enum.Enum):
    WALL = Boundaries(
        on_entry=dict(up=False, right=False, down=False, left=False),
        on_exit=dict(up=False, right=False, down=False, left=False)
        )
    FLOOR = Boundaries(
        on_entry=dict(up=True, right=True, down=True, left=True),
        on_exit=dict(up=True, right=True, down=True, left=True)
        )
    SEAT = Boundaries(
        on_entry=dict(up=True, right=True, down=False, left=True),
        on_exit=dict(up=True, right=True, down=False, left=True)
        )
    EXIT = Boundaries(
        on_entry=dict(up=True, right=True, down=True, left=True),
        on_exit=dict(up=False, right=False, down=False, left=False)
        )


def visualisation(layout, cost, occupancy):
    grid = Grid(layout, cost, occupancy)
    while sum(sum(grid.occupancy)) > 0:
        pyplot.ion()
        pyplot.clf()
        pyplot.matshow(grid.occupancy, fignum=0, cmap='binary')
        pyplot.show()
        grid.make_step()
        pyplot.pause(0.0000005)


def timer(grid):
    """Count of total time steps to evacuate plane."""

    count = 0
    while sum(sum(grid.occupancy)) > 0:
        grid.make_step()
        if grid.leaving == 1:
            count += .475
        else:
            count += .312
    return count


def multi_timer(layout, cost, occupancy, n=100):
    """Returns list of n time results from timer."""

    count_list = []
    for i in range(n):
        o = copy.copy(occupancy)
        grid = Grid(layout, cost, o)
        count_list.append(timer(grid))
    return count_list
