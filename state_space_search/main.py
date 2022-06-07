from utils import grid_from_file
from solver import *
from pprint import pprint

if __name__ == '__main__':
    level = grid_from_file("maps/tests/corridor.txt")
    map_, state = parse_grid(level)
    states = solve(state, map_, actions_factories)
    pprint(states)



