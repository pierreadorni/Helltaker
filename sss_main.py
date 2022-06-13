""" Main script to execute State Space Search solver"""
import sys
from typing import List

from utils import grid_from_file
from state_space_search.solver import (
    solve_a_star,
    parse_grid,
    is_valid,
    helltaker_actions_factories,
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
    plan = solve_a_star(state, _map, helltaker_actions_factories)
    formatted_plan = format_plan(plan)

    # affichage du résultat
    if is_valid(_map, state, helltaker_actions_factories, plan):
        print("[OK]", formatted_plan)
    else:
        print("[Err]", formatted_plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
