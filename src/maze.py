from time import sleep
from window import Window
from cell import Cell


class Maze:
    """Represents a 2D maze that can be drawn and animated on the parent ``Window``"""

    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_width: int,
        cell_height: int,
        window: Window | None = None,
    ) -> None:
        """Creates a new 2D maze parented to the specified ``Window``.

        Args:
            win (Window | None): The parent window to draw the maze on.
            x1 (int): The X coordinate of the top-left corner of the maze.
            y1 (int): The Y coordinate of the top-left corner of the maze.
            num_rows (int): The number of rows of cells in the maze.
            num_cols (int): The number of columns of cells in the maze.
            cell_width (int): The number of pixels wide each cell should be.
            cell_height (int): The number of pixels high each cell should be.
        """
        if num_rows == 0 or num_cols == 0:
            raise ValueError("Maze must have at least 1 row and 1 column")
        if cell_height <= 0 or cell_width <= 0:
            raise ValueError("Maze cells must be at least 1 pixel wide and 1 pixel tall")
        self._win = window
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
        animates the drawing. If no Window is provided at construction, this
        function is a no-op.

        Args:
            i (int): The column of the cell to draw
            j (int): The row of the cell to draw
        """
        if self._win is None:
            return
        cell_x1 = self._x1 + self._cell_width * i
        cell_y1 = self._y1 + self._cell_height * j
        cell_x2 = cell_x1 + self._cell_width
        cell_y2 = cell_y1 + self._cell_height
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self) -> None:
        """Redraws the parent ``Window`` and pauses for a short delay, to allow
        for a consistent framerate rather than instantaneous drawing. If no
        Window is provided at construction, this function is a no-op."""
        if self._win is None:
            return
        self._win.redraw()
        sleep(1 / 25)
