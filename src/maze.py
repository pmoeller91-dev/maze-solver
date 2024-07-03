from time import sleep
from window import Window
from cell import Cell


class Maze:
    """Represents a 2D maze that can be drawn and animated on the parent ``Window``"""

    def __init__(
        self,
        win: Window,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_width: int,
        cell_height: int,
    ) -> None:
        """Creates a new 2D maze parented to the specified ``Window``.

        Args:
            win (Window): The parent window to draw the maze on.
            x1 (int): The X coordinate of the top-left corner of the maze.
            y1 (int): The Y coordinate of the top-left corner of the maze.
            num_rows (int): The number of rows of cells in the maze.
            num_cols (int): The number of columns of cells in the maze.
            cell_width (int): The number of pixels wide each cell should be.
            cell_height (int): The number of pixels high each cell should be.
        """
        self._win = win
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._cells: list[list[Cell]] = []
        self._create_cells()

    def _create_cells(self) -> None:
        """Initializes all the cells in the maze and then draws them."""
        for x in range(self._num_cols):
            self._cells.append([])
            for y in range(self._num_rows):
                self._cells[x].append(Cell(self._win))
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        """Draws a single cell based on its column and row within the maze, and
        animates the drawing.

        Args:
            i (int): The column of the cell to draw
            j (int): The row of the cell to draw
        """
        cell_x1 = self._x1 + self._cell_width * i
        cell_y1 = self._y1 + self._cell_height * j
        cell_x2 = cell_x1 + self._cell_width
        cell_y2 = cell_y1 + self._cell_height
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self) -> None:
        """Redraws the parent ``Window`` and pauses for a short delay, to allow
        for a consistent framerate rather than instantaneous drawing"""
        self._win.redraw()
        sleep(1 / 25)
