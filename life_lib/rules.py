import abc
from typing import Callable


class RulesInterface:
    """Interface for determination of n+1 state.

    Can be used as 'plugin' to inject new functionality into game of life.
    """
    @classmethod
    @abc.abstractmethod
    def get_next_value(cls, y_idx, x_idx, gf_state: Callable[[int, int], bool]) -> bool:
        """Given x, y coordinates and handle to determine state of other coordinates,
           return next state of the cell."""


class ClassicRules(RulesInterface):
    """Using the classic GOL rules, determine next state of cell.

    source: http://pi.math.cornell.edu/~lipa/mec/lesson6.html
    * If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
    * If the cell is dead, then it springs to life only in the case that it has 3 live neighbors
    """
    OFFSETS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    @classmethod
    def _get_live_neighbors(cls, y_idx: int, x_idx: int,
                            gf_state: Callable[[int, int], bool]) -> int:
        live_neighbors = 0
        for offset in cls.OFFSETS:
            try:
                if gf_state(y_idx + offset[0], x_idx + offset[1]):
                    live_neighbors += 1
            except IndexError:
                # For now, our board is bounded w/o periodic boundary conditions
                pass
        return live_neighbors

    @classmethod
    def get_next_value(cls, y_idx: int, x_idx:int,
                       gf_state: Callable[[int, int], bool]) -> bool:
        live_neighbors = cls._get_live_neighbors(y_idx, x_idx, gf_state)

        is_alive = gf_state(y_idx, x_idx)

        if is_alive and live_neighbors in (2, 3):
            return True
        if not is_alive and live_neighbors == 3:
            return True
        return False


class HighLifeRules(ClassicRules):
    """Using the classic GOL rules, determine next state of cell.

    source: https://www.conwaylife.com/wiki/Conway%27s_Game_of_Life#Variations_on_Life
    * If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
    * If the cell is dead, then it springs to life if it has 3 or 6 neighbors
    """

    @classmethod
    def get_next_value(cls, y_idx, x_idx, gf_state: Callable[[int, int], bool]) -> bool:
        live_neighbors = cls._get_live_neighbors(y_idx, x_idx, gf_state)

        is_alive = gf_state(y_idx, x_idx)

        if is_alive and live_neighbors in (2, 3):
            return True
        if not is_alive and live_neighbors in (3, 6):
            return True
        return False
