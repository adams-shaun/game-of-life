"""Class represents one iteration in the game of life."""

from typing import List, Tuple, Type

from life_lib.rules import RulesInterface


class GameFrame:
    """Object represents one frame in the game of life sequence.

    Instantiate board with dimensions and initial conditions.
    For ex:
      initial_conditions = [(1, 2)]  (y, x)
    Represents one cell in the second row and third column of the grid.

    Internally, we instantiate a grid as one dimensional array
         ^
         | G H I
         | D E F
     (y) | A B C
         --------->
          (x)
    --> A B C D E F G H I
    For the element at (1, 1), the index would be width*y + x
    i.e. 1 * 3 + 1 = 4, which gives the fifth element ('E')
    """

    def __init__(self,
                 height: int,
                 width: int,
                 initial_conditions: List[Tuple[int, int]]):
        self._height = height
        self._width = width
        self._initial_conditions = initial_conditions

        # I've found 1d array to be easier to work with for similar problems in the past.
        # It probably doesn't matter much.
        self._cells = [False] * (width * height)

        # update cells with initial conditions
        for item in initial_conditions:
            # I don't love the (y, x) notation, because it deviates from norm, but
            #  due to time constraints we are going with it.
            y_pos = item[0]
            x_pos = item[1]

            # I'm not huge on checking *every* possible invalid input
            # there are after-all, great static analysis tools which can highlight typing issues
            # but for something like integer ranges, it seems like an easily implemented guard rail.
            if x_pos < 0 or x_pos >= width:
                raise ValueError(f'Invalid initial condition supplied: {item}')
            if y_pos < 0 or y_pos >= height:
                raise ValueError(f'Invalid initial condition supplied: {item}')
            self._cells[self._get_cell_index(y_pos, x_pos)] = True

    def _get_cell_index(self, y_idx: int, x_idx: int) -> int:
        """Performs translation of cartesian coordinates to 1d cells index."""
        return y_idx * self._width + x_idx

    def _get_index_coords(self, cell_index: int) -> Tuple[int, int]:
        """Performs translation from cell index to cartesian coordinates."""
        y_idx = cell_index // self._height
        x_idx = cell_index % self._width
        return y_idx, x_idx

    def _get_cell_value(self, y_idx: int, x_idx: int) -> bool:
        # Without this checking, our nested math would be broken.
        # If we were enforcing periodic boundary conditions, this would be more complex.
        if y_idx < 0 or y_idx >= self._height:
            raise IndexError('Over the line')
        if x_idx < 0 or x_idx >= self._width:
            raise IndexError('Mark it 0')
        return self._cells[self._get_cell_index(y_idx, x_idx)]

    def gen_next(self, rules: Type[RulesInterface]) -> 'GameFrame':
        """For each cell, apply rules to determine next state.

        Code is structure this way such that rules object could be modified independent of this class.
        Implementation in this fashion means, in effect, the GameFrame objects are immutable.
        I took this approach from a recent reading (https://eloquentjavascript.net/07_robot.html)
        and figured I would explore implementation in this little project.
        """
        next_initial_conditions = []

        for idx in range(len(self._cells)):
            y_idx, x_idx = self._get_index_coords(idx)
            if rules.get_next_value(y_idx, x_idx, self._get_cell_value):
                next_initial_conditions.append((y_idx, x_idx))

        return GameFrame(self._height, self._width, next_initial_conditions)

    def __str__(self) -> 'str':
        """Printable GameFrame.

        Mainly used for debugging/visualization.
        Probably should have a repr for other uses.

        `#` denotes alive cell, '-' denotes a dead cell
        """
        def _bool_to_char(value: bool):
            if value:
                return '#'
            return '-'

        lines = []
        for y_idx in range(self._height):
            line_chars = [_bool_to_char(val) for val in self._cells[y_idx * self._width: (y_idx + 1) * self._width]]
            line = ' '.join(line_chars)
            lines.append(line)
        lines.reverse()
        return '\n'.join(lines)

    def __eq__(self, other):
        return self._cells == other._cells  # pylint: disable...
