import unittest
from unittest import mock
import time

from life_lib.engine import GameRunner


class TestGameRunner(unittest.TestCase):
    def setUp(self):
        self.height = 20
        self.width = 20
        self.init_cond = []
        self.steps = 13

    @mock.patch.object(time, 'sleep')
    def test_execute(self, mock_sleep):
        runner = GameRunner(self.height, self.width, self.steps, self.init_cond)
        runner.execute()
        assert mock_sleep.call_count == self.steps

