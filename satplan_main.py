import sys
from utils import grid_from_file, check_plan
from satplan.SatSolver import creation_cnf, sat_solver


def main():
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de la grille et de toutes les infos
    infos = grid_from_file(filename)

    # création du cnf
    cnf = creation_cnf(sat_solver(infos))

    # calcul du plan
    # call subprocess with gophersat
    plan = "hbgf"

    # affichage du résultat
    if check_plan(plan):
        print("[OK]", plan)
    else:
        print("[Err]", plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
