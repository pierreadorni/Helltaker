from utils import grid_from_file
from state_space_search.solver import *
from satplan.SatSolver import creation_cnf, sat_solver
from pprint import pprint


def state_space_search():
    """ Test for state space search """
    level = grid_from_file("maps/tests/corridor.txt")
    map_, state = parse_grid(level)
    states = solve(state, map_, actions_factories)
    pprint(states)


def satplan():
    """ Test for satplan """
    infos = grid_from_file("maps/tests/corridor.txt")
    cnf = creation_cnf(sat_solver(infos))
    print(cnf)


if __name__ == '__main__':
    state_space_search()
    satplan()


