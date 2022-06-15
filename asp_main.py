""" Main script to execute SAP solver"""
import sys
from typing import List
import subprocess

from utils import grid_from_file
from asp_solver.creation_asp import creation_map, exec_asp,formater_chemin


def main():
    """Main script to execute State Space Search solver"""
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de la grille et de toutes les infos
    infos = grid_from_file(filename)

    # realisation du plan
    sap = creation_map(infos)
    with open("solver_asp.lp", "w") as f:
        f.write(sap)

    result = subprocess.run(
        ["clingo", "Helltaker\solver_asp.lp"], capture_output=True
    ).stdout.decode("utf-8")


    chemin = result.split("\n")[4]
    print(formater_chemin(chemin))



if __name__ == "__main__":
    main()
