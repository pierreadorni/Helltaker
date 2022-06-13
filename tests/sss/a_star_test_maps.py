import unittest
from state_space_search.solver import (
    parse_grid,
    helltaker_actions_factories,
    solve_a_star,
    is_valid,
)
from utils import grid_from_file


class TestMapsAStar(unittest.TestCase):
    def _test_file(self, filename: str):
        level = grid_from_file(filename)
        map_, state = parse_grid(level)
        plan = solve_a_star(state, map_, helltaker_actions_factories)
        print(plan)
        self.assertTrue(is_valid(map_, state, helltaker_actions_factories, plan))

    def test_corridor(self):
        self._test_file("maps/tests/corridor.txt")

    def test_locknkey(self):
        self._test_file("maps/tests/locknkey.txt")

    def test_spikes1(self):
        self._test_file("maps/tests/spikes1.txt")

    def test_traps1(self):
        self._test_file("maps/tests/traps1.txt")
