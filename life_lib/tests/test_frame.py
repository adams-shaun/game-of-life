import unittest
from unittest import mock
import time

from life_lib.frame import GameFrame
from life_lib.rules import ClassicRules


class TestGameFrame(unittest.TestCase):
    def setUp(self):
        self.height = 5
        self.width = 5
        self.init_cond = [
            (0, 0), (0, 1), (1, 0), (1, 1)
        ]
        self.steps = 10
        self.gf = GameFrame(self.height, self.width, self.init_cond)

    def test_instantiation_oob(self):
        bad_init_cond = [
            (5, 5)
        ]
        try:  # with pytest.raises()
            GameFrame(self.height, self.width, bad_init_cond)
            raise Exception('I should not be here')
        except ValueError:
            pass

    def test_get_cell_index(self):
        # more, if time allowed
        assert self.gf._get_cell_index(4, 4) == 24

    def test_get_index_coords(self):
        # more, if time allowed
        assert self.gf._get_index_coords(24) == (4, 4)

    def test_get_cell_value_true(self):
        assert self.gf._get_cell_value(1, 1) is True

    def test_get_cell_value_false(self):
        assert self.gf._get_cell_value(2, 2) is False

    def test_gen_next(self):
        new_gf = self.gf.gen_next(ClassicRules)

        # Overloaded == operator for this, no consideration as to height and width though...
        assert new_gf == self.gf