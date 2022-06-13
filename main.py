from utils import grid_from_file
from satplan.SatSolver import creation_cnf, sat_solver


def satplan():
    """Test for satplan"""
    infos = grid_from_file("maps/tests/corridor.txt")
    cnf = creation_cnf(sat_solver(infos))
    print(cnf)


if __name__ == "__main__":
    satplan()
