import random
from enum import Enum
from time import sleep
from window import Window
from cell import Cell


class Direction(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


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
        seed: int | float | str | bytes | bytearray | None = None,
    ) -> None:
        """Creates a new 2D maze parented to the specified ``Window``.

        Args:
            x1 (int): The X coordinate of the top-left corner of the maze.
            y1 (int): The Y coordinate of the top-left corner of the maze.
            num_rows (int): The number of rows of cells in the maze.
            num_cols (int): The number of columns of cells in the maze.
            cell_width (int): The number of pixels wide each cell should be.
            cell_height (int): The number of pixels high each cell should be.
            window (Window | None): The parent window to draw the maze on.
            seed (int | float | str | bytes | bytearray | None): The seed used
            to generate the maze. If ``None``, no initial seed will be used.
            Defaults to ``None``.

        Raises:
            ValueError: Raises ValueError if:
              - ``num_rows`` or ``num_cols`` are not at least 1.
              - ``cell_height`` or ``cell_width`` are not at least 1.
        """
        if seed is not None:
            random.seed(seed)
        if num_rows <= 0 or num_cols <= 0:
            raise ValueError("Maze must have at least 1 row and 1 column")
        if cell_height <= 0 or cell_width <= 0:
            raise ValueError(
                "Maze cells must be at least 1 pixel wide and 1 pixel tall"
            )
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
        Window is provided at construction, this function is a no-op.
        """
        if self._win is None:
            return
        self._win.redraw()
        sleep(1 / 25)

    def _break_entrance_and_exit(self) -> None:
        """Break the entrance and exit walls. Entry is always the top wall of
        the top-left-most cell, and exit is always the bottom of the
        bottom-right-most cell.
        """
        entry_cell = self._cells[0][0]
        entry_cell.has_top_wall = False
        self._draw_cell(0, 0)
        exit_cell = self._cells[-1][-1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_cells_r(self, i: int, j: int) -> None:
        """Recursively visit cells and break walls in a random direction, until
        every cell in the maze has been visited.

        Args:
            i (int): X index of the current cell.
            j (int): Y index of the current cell.
        """
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            cells_to_visit = self._get_visitable_cells(i, j)
            if len(cells_to_visit) == 0:
                self._draw_cell(i, j)
                break
            direction, vi, vj = cells_to_visit[random.randrange(0, len(cells_to_visit))]
            visit_cell = self._cells[vi][vj]
            match direction:
                case Direction.UP:
                    current_cell.has_top_wall = False
                    visit_cell.has_bottom_wall = False
                case Direction.RIGHT:
                    current_cell.has_right_wall = False
                    visit_cell.has_left_wall = False
                case Direction.DOWN:
                    current_cell.has_bottom_wall = False
                    visit_cell.has_top_wall = False
                case Direction.LEFT:
                    current_cell.has_left_wall = False
                    visit_cell.has_right_wall = False
            self._break_cells_r(vi, vj)

    def _get_visitable_cells(self, i: int, j: int) -> list[tuple[Direction, int, int]]:
        """Gets visitable cells adjacent to a given cell. Cell is only visitable
        if it has not already been ``visited``.

        Args:
            i (int): X index of the cell.
            j (int): Y index of the cell.

        Raises:
            ValueError: Raises ValueError if ``i`` or ``j`` are out of bounds
            based on the maze's number of columns or rows.

        Returns:
            list[tuple[Direction, int, int]]: A list of visitable cells, along
            with the direction relative to the base cell.
        """
        last_col = self._num_cols - 1
        last_row = self._num_rows - 1

        if i > last_col or j > last_row or i < 0 or j < 0:
            raise ValueError(f"Invalid cell index provided: ({i}, {j})")

        visitable_cells: list[tuple[int, int]] = []

        # Up
        if j >= 1 and not self._cells[i][j - 1].visited:
            visitable_cells.append((Direction.UP, i, j - 1))

        # Right
        if (i + 1) <= last_col and not self._cells[i + 1][j].visited:
            visitable_cells.append((Direction.RIGHT, i + 1, j))

        # Down
        if (j + 1) <= last_row and not self._cells[i][j + 1].visited:
            visitable_cells.append((Direction.DOWN, i, j + 1))

        # Left
        if i >= 1 and not self._cells[i - 1][j].visited:
            visitable_cells.append((Direction.LEFT, i - 1, j))

        return visitable_cells
