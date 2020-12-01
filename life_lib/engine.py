"""Represents the game-runner.  Used to take imput, execute to completion."""

import time
import typing

from life_lib import rules, frame


class GameRunner:
    def __init__(self, height: int, width: int, num_steps: int,
                 initial_conditions: typing.List[typing.Tuple[int, int]],
                 pause_time_msec: int = 500,
                 rule_engine=rules.ClassicRules):
        self._height = height
        self._width = width
        self._num_steps = num_steps
        self._rule_engine = rule_engine
        self._pause_time: float = pause_time_msec / 1000
        self._initial_conditions = initial_conditions

    def execute(self):
        curr_frame = frame.GameFrame(self._height, self._width, self._initial_conditions)
        for idx in range(self._num_steps):
            print(f"Iteration {idx + 1}:\n{curr_frame}")
            time.sleep(self._pause_time)
            curr_frame = curr_frame.gen_next(self._rule_engine)
