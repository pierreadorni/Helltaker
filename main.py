from utils import grid_from_file
from state_space_search.solver import *
from satplan.SatSolver import creation_cnf, sat_solver, exam
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
    with open('clauses.cnf', 'w') as f:
        f.write(cnf)
    #print(cnf)
    result = subprocess.run(["gophersat", "clauses.cnf"], capture_output=True).stdout.decode("utf-8")
    with open('solve.cnf', 'w') as f:
        f.write(result)
    exam('clauses.cnf', 'solve.cnf', sat[2])


if __name__ == "__main__":
    state_space_search()
    satplan()
