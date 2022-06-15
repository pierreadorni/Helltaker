""" ASP Tests file """
import unittest

from asp.creationMapASP import creation_map, exec_asp
from utils import grid_from_file


class TestMapsASP(unittest.TestCase):
    def _test_file(self, filename: str, answer: str):
        infos = grid_from_file(filename)
        asp_code = creation_map(infos)
        with open("solver_asp.lp", "w", encoding="utf-8") as f:
            f.write(asp_code)
        chemin = exec_asp("solver_asp.lp")
        self.assertEqual(chemin, answer)

    def test_corridor(self):
        self._test_file("maps/tests/corridor.txt", "bbb")

    def test_locknkey(self):
        self._test_file("maps/tests/locknkey.txt", "gggddddddddd")

    def test_spikes1(self):
        self._test_file("maps/tests/spikes1.txt", "dbddh")

    def test_traps1(self):
        self._test_file("maps/tests/traps1.txt", "hddd")


if __name__ == "__main__":
    unittest.main()
