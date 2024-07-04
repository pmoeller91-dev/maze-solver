from typing_extensions import Self
from window import Window
from point import Point
from line import Line

_cell_color = "black"
_absent_color = "#d9d9d9"


class Cell:
    """Represents a single cell in a maze, which can have coordinates and some
    configuration of walls.

    Attributes:
        has_top_wall (bool): Whether the cell has a top wall
        has_right_wall (bool): Whether the cell has a right wall
        has_bottom_wall (bool): Whether the cell has a bottom wall
        has_left_wall (bool): Whether the cell has a left wall
        visited (bool): Whether the cell has been visited yet during maze generation.
    """

    def __init__(
        self,
        window: Window | None = None,
        has_top_wall: bool = True,
        has_right_wall: bool = True,
        has_bottom_wall: bool = True,
        has_left_wall: bool = True,
    ) -> None:
        """Create a new cell representing a cell in a maze.

        Args:
            window (Window | None): The parent window the cell will be drawn in.
            Defaults to None.
            has_top_wall (bool, optional): Whether the cell starts with a top wall. Defaults to True.
            has_right_wall (bool, optional): Whether the cell starts with a right wall. Defaults to True.
            has_bottom_wall (bool, optional): Whether the cell starts with a bottom wall. Defaults to True.
            has_left_wall (bool, optional): Whether the cell starts with a left wall. Defaults to True.
        """
        self._window = window
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self.has_top_wall = has_top_wall
        self.has_right_wall = has_right_wall
        self.has_bottom_wall = has_bottom_wall
        self.has_left_wall = has_left_wall
        self.visited = False

    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Draws the cell to the parent canvas at the specified coordinates. If
        constructed with no Window, this function changes the coordinates but
        otherwise is a no-op.

        Args:
            x1 (int): X-coordinate of the top-left corner of the cell.
            y1 (int): Y-coordinate of the top-left corner of the cell.
            x2 (int): X-coordinate of the bottom-right corner of the cell.
            y2 (int): Y-coordinate of the bottom-right corner of the cell.
        """
        window = self._window
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2
        if window is None:
            return

        top = Line(Point(x1, y1), Point(x2, y1))
        right = Line(Point(x2, y1), Point(x2, y2))
        bottom = Line(Point(x1, y2), Point(x2, y2))
        left = Line(Point(x1, y1), Point(x1, y2))

        window.draw_line(top, _absent_color)
        window.draw_line(right, _absent_color)
        window.draw_line(bottom, _absent_color)
        window.draw_line(left, _absent_color)

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            window.draw_line(line, _cell_color)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            window.draw_line(line, _cell_color)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            window.draw_line(line, _cell_color)
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            window.draw_line(line, _cell_color)

    def draw_move(self, to_cell: Self, undo=False):
        """Draw a move from one cell to another in the maze. Red by default,
        grey if it is a move that was undone. If constructed without a ``Window``,
        this function is a no-op.

        Args:
            to_cell (Self): The cell to draw the move to
            undo (bool, optional): Whether the move is an undone move. Defaults to False.
        """
        if self._window is None:
            return
        color = "red" if undo is False else "gray"
        center = (Point(self._x1, self._y1) + Point(self._x2, self._y2)) // 2
        other_center = (
            Point(to_cell._x1, to_cell._y1) + Point(to_cell._x2, to_cell._y2)
        ) // 2
        move_line = Line(center, other_center)
        self._window.draw_line(move_line, fill_color=color)
