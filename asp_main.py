""" Main script to execute ASP solver"""
import sys
from typing import List

from asp.creationMapASP import creation_map, exec_asp
from utils import grid_from_file, check_plan
from state_space_search import (
    solve_a_star,
    parse_grid,
    is_valid,
    helltaker_actions_factories,
    helltaker_directions,
)


def format_plan(plan: List[str]):
    """Format the plan to be automatically tested"""
    formatted_plan = ""
    directions = {
        "left": "g",
        "right": "d",
        "top": "h",
        "bottom": "b",
    }
    for action in plan:
        formatted_plan += directions[action.split("_")[-1]]
    return formatted_plan


def main():
    """Main script to execute State Space Search solver"""
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de la grille et de toutes les infos
    infos = grid_from_file(filename)
    _map, state = parse_grid(infos)

    # calcul du plan
    asp_code = creation_map(infos)
    with open("solver_asp.lp", "w", encoding="utf-8") as f:
        f.write(asp_code)
    formatted_plan = exec_asp("solver_asp.lp")

    # affichage du résultat
    if check_plan(formatted_plan):
        print("[OK]", formatted_plan)
    else:
        print("[Err]", formatted_plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
