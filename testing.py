import cellular_automata.cellular_automata_group
from cellular_automata.cellular_automata_group import *
import dataclasses
import enum
import numpy as np

c = np.array([[-1, 15, 14, 13, 12, 13, 14, 15, -1],
              [-1, 14, 13, 12, 11, 12, 13, 14, -1],
              [-1, 13, 12, 11, 10, 11, 12, 13, -1],
              [-1, 12, 11, 10,  9, 10, 11, 12, -1],
              [-1, 11, 10,  9,  8,  9, 10, 11, -1],
              [-1, 10,  9,  8,  7,  8,  9, 10, -1],
              [-1, -1, -1, -1,  6, -1, -1, -1, -1],
              [-1, -1, -1, -1,  5, -1, -1, -1, -1],
              [0,  1,  2,  3,  4,  3,  2,  1,  0]])
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
# while True:
o = np.array([[False, True, True, True, False, True, True, True, False],
                [False, True, True, True, False, True, True, True, False],
                [False, True, True, True, False, True, True, True, False],
                [False, True, True, True, False, True, True, True, False],
                [False, True, True, True, False, True, True, True, False],
                [False, True, True, True, False, True, True, True, False],
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False]])
cellular_automata.cellular_automata_group.visualisation(l, c, o)
multi_timer(l, c, o)
