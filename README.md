# cellular_automata
## Introduction
Cellular automata is a simplistic agent-based model of pedestrian dynamics. It uses a cellular representation of space and often operates on discrete time steps. Using simple rules for each agent's movement, complicated crowd behaviours can often arise. This project is a proof-of-concept implementation of cellular automata in python, aiming at simulating plane evacuations (but can be generalised) and providing a visual output in real-time.
## How to use
The space is represented by the `Grid` class, with three grids of matching dimensions representing:
* Layout: The properties of all cells, mainly the accessibility. Four different types of cells were implemented in our model, encapsulated in the `Cell` enum.
* Cost/Distance: The distance of the cell to the closest `EXIT`. For all inaccessible cells, the distance is `-1`. Currently this has to be manually mapped.
* Occupancy: Whether a cell is occupied by an agent at the start of simulation or not. 
For simulation, simply pass the three grids to the visualisation function:
```Python
import cellular_automata.cellular_automata_group
from cellular_automata.cellular_automata_group import *
...
layout = ...
cost = ...
occupancy = ...
cellular_automata.cellular_automata_group.visualisation(layout, cost, occupancy)
```
## Demo
A demo is provided within `testing.py`, using the rear of an Airbus A320 European layout as a sample.
