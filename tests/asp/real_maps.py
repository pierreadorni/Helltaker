""" ASP Tests file """
import unittest

from asp.creationMapASP import creation_map, exec_asp
from state_space_search import (
    create_actions,
    helltaker_directions,
    helltaker_actions_factories,
    parse_grid,
    PrecondNotMetException,
    execute,
    is_valid,
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


class RealMapsASP(unittest.TestCase):
    def _test_file(self, filename: str):
        infos = grid_from_file(filename)
        _map, state = parse_grid(infos)
        asp_code = creation_map(infos)
        with open("solver_asp.lp", "w", encoding="utf-8") as f:
            f.write(asp_code)
        chemin = exec_asp("solver_asp.lp")
        self.assertTrue(
            is_valid(
                _map,
                state,
                helltaker_actions_factories,
                helltaker_directions,
                str_plan_to_actions_names(chemin, filename),
            )
        )

    def test_level1(self):
        self._test_file("maps/level1.txt")

    def test_level2(self):
        self._test_file("maps/level2.txt")

    def test_level3(self):
        self._test_file("maps/level3.txt")

    def test_level4(self):
        self._test_file("maps/level4.txt")

    def test_level5(self):
        self._test_file("maps/level5.txt")

    def test_level6(self):
        self._test_file("maps/level6.txt")

    def test_level7(self):
        self._test_file("maps/level7.txt")

    def test_level8(self):
        self._test_file("maps/level8.txt")

    def test_level9(self):
        self._test_file("maps/level9.txt")


if __name__ == "__main__":
    unittest.main()
