import unittest
from state_space_search import (
    parse_grid,
    helltaker_actions_factories,
    solve,
    is_valid,
    helltaker_directions,
)
from utils import grid_from_file


class RealMaps(unittest.TestCase):
    def _test_file(self, filename: str):
        level = grid_from_file(filename)
        map_, state = parse_grid(level)
        plan = solve(state, map_, helltaker_actions_factories)
        print(plan)
        self.assertTrue(
            is_valid(
                map_, state, helltaker_actions_factories, helltaker_directions, plan
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
