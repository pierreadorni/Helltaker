""" ASP Tests file """
import unittest

from asp.creationMapASP import creation_map, exec_asp
from state_space_search import (
    parse_grid,
    create_actions,
    helltaker_directions,
    execute,
    PrecondNotMetException,
    is_valid,
    helltaker_actions_factories,
)
from utils import grid_from_file


def str_plan_to_actions_names(str_plan: str, filename: str) -> list:
    """
    Convert a string plan to a list of actions names
    """
    grid = grid_from_file(filename)
    _map, state = parse_grid(grid)
    actions_names = []
    actions = create_actions(helltaker_actions_factories, _map, helltaker_directions)
    translation = {
        "h": "top",
        "b": "bottom",
        "g": "left",
        "d": "right",
    }
    for red_action in str_plan:
        for action in actions:
            if action.endswith(translation[red_action]):
                try:
                    state = execute(state, actions[action])
                except PrecondNotMetException:
                    continue
                actions_names.append(action)
                break
    return actions_names


class TestMapsASP(unittest.TestCase):
    def _test_file(self, filename: str):
        infos = grid_from_file(filename)
        _map, state = parse_grid(infos)
        asp_code = creation_map(infos)
        with open("solver_asp.lp", "w", encoding="utf-8") as f:
            f.write(asp_code)
        chemin = exec_asp("solver_asp.lp")
        print(str_plan_to_actions_names(chemin, filename))
        self.assertTrue(
            is_valid(
                _map,
                state,
                helltaker_actions_factories,
                helltaker_directions,
                str_plan_to_actions_names(chemin, filename),
            )
        )

    def test_corridor(self):
        self._test_file("maps/tests/corridor.txt")

    def test_locknkey(self):
        self._test_file("maps/tests/locknkey.txt")

    def test_spikes1(self):
        self._test_file("maps/tests/spikes1.txt")

    def test_traps1(self):
        self._test_file("maps/tests/traps1.txt")


if __name__ == "__main__":
    unittest.main()
