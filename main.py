from utils import grid_from_file
from state_space_search.solver import *
from satplan.SatSolver import creation_cnf, sat_solver, solutionner
from pprint import pprint
from asp.creationMapASP import creation_map, exec_asp
import subprocess
import clingo


def state_space_search():
    """Test for state space search"""
    level = grid_from_file("maps/tests/corridor.txt")
    map_, state = parse_grid(level)
    states = solve(state, map_, actions_factories)
    pprint(states)


def sapplan():
    """Test for asp solver"""
    infos = grid_from_file("maps/level8.txt")
    sap = creation_map(infos)
    with open("solver_asp.lp", "w") as f:
        f.write(sap)
    exec_asp("solver_asp.lp")


if __name__ == "__main__":
    # state_space_search()
    print(sapplan())

