from utils import grid_from_file
from state_space_search.solver import *
from satplan.SatSolver import creation_cnf, sat_solver, solutionner
from satplan.SatSolver2 import solve_laby2
from pprint import pprint
import subprocess

def state_space_search():
    """Test for state space search"""
    level = grid_from_file("maps/tests/corridor.txt")
    map_, state = parse_grid(level)
    states = solve(state, map_, actions_factories)
    pprint(states)


def satplan():
    """Test for satplan"""
    infos = grid_from_file("maps/tests/corridor.txt")
    sat = sat_solver(infos)
    cnf = creation_cnf(sat)
    # je vais mettre ca dans le satsolver
    with open("clauses.cnf", "w") as f:
        f.write(cnf)
    # print(cnf)
    result = subprocess.run(
        ["gophersat", "clauses.cnf"], capture_output=True
    ).stdout.decode("utf-8")
    with open("solve.cnf", "w") as f:
        f.write(result)
    solutionner("solve.cnf", sat[2])

def satplan2():

    """Test for satplan"""
    infos = grid_from_file("maps/tests/corridor.txt")
    sat = solve_laby2(infos)
    print(sat)



if __name__ == "__main__":
    # state_space_search()
    satplan2()
