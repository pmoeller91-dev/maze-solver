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

    def _break_walls_r(self, i: int, j: int) -> None:
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
            self._break_walls_r(vi, vj)

    def _get_visitable_cells(
        self, i: int, j: int, ignore_walls: bool = True
    ) -> list[tuple[Direction, int, int]]:
        """Gets visitable cells adjacent to a given cell. Cell is only visitable
        if it has not already been ``visited``.

        Args:
            i (int): X index of the cell.
            j (int): Y index of the cell.
            ignore_walls (bool): Whether to ignore walls when accounting for
            whether a cell should be visitable. Defaults to ``True``, as in the
            case for maze generation.

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
        if self._can_visit_direction(i, j, Direction.UP, ignore_walls):
            visitable_cells.append((Direction.UP, i, j - 1))

        # Right
        if self._can_visit_direction(i, j, Direction.RIGHT, ignore_walls):
            visitable_cells.append((Direction.RIGHT, i + 1, j))

        # Down
        if self._can_visit_direction(i, j, Direction.DOWN, ignore_walls):
            visitable_cells.append((Direction.DOWN, i, j + 1))

        # Left
        if self._can_visit_direction(i, j, Direction.LEFT, ignore_walls):
            visitable_cells.append((Direction.LEFT, i - 1, j))

        return visitable_cells

    def _can_visit_direction(
        self, i: int, j: int, direction: Direction, ignore_walls: bool = True
    ) -> bool:
        """Checks whether the cell at the given index can visit a cell in the
        given direction. When ``ignore_walls`` is True, ``True`` if a cell
        exists in the direction, and the cell has not been visited. When
        ``ignore_walls`` is False, ``True`` if a cell exists in the direction,
        the cell has not been visited, and no walls exist between the two cells.

        Args:
            i (int): The X index of the base cell
            j (int): The Y index of the base cell
            direction (Direction): The direction to check for a valid cell in
            ignore_walls (bool, optional): Whether to ignore walls or not when
            performing the check. Defaults to True.

        Raises:
            ValueError: Raises a ``ValueError`` if ``i`` or ``j`` are out of
            range of the number of columns and rows in the maze.

        Returns:
            bool: Whether or not the cell in ``direction`` can be visited
        """
        last_col = self._num_cols - 1
        last_row = self._num_rows - 1

        if i > last_col or j > last_row or i < 0 or j < 0:
            raise ValueError(f"Invalid cell index provided: ({i}, {j})")

        current_cell = self._cells[i][j]

        match direction:
            case Direction.UP:
                if j <= 0:
                    return False
                up_cell = self._cells[i][j - 1]
                if up_cell.visited:
                    return False
                if ignore_walls:
                    return True
                if not current_cell.has_top_wall and not up_cell.has_bottom_wall:
                    return True
                else:
                    return False
            case Direction.RIGHT:
                if i >= last_col:
                    return False
                right_cell = self._cells[i + 1][j]
                if right_cell.visited:
                    return False
                if ignore_walls:
                    return True
                if not current_cell.has_right_wall and not right_cell.has_left_wall:
                    return True
                else:
                    return False
            case Direction.DOWN:
                if j >= last_row:
                    return False
                down_cell = self._cells[i][j + 1]
                if down_cell.visited:
                    return False
                if ignore_walls:
                    return True
                if not current_cell.has_bottom_wall and not down_cell.has_top_wall:
                    return True
                else:
                    return False
            case Direction.LEFT:
                if i <= 0:
                    return False
                left_cell = self._cells[i - 1][j]
                if left_cell.visited:
                    return False
                if ignore_walls:
                    return True
                if not current_cell.has_left_wall and not left_cell.has_right_wall:
                    return True
                else:
                    return False

    def _reset_cells_visited(self) -> None:
        """Reset the visited property of all cells to ``False``, to setup for
        maze solving.
        """
        for col in self._cells:
            for row in col:
                row.visited = False

    def generate_maze(self) -> None:
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def solve(self) -> bool:
        """Animate solving the current maze.

        Returns:
            bool: Whether the maze was solved successfully or not.
        """
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:
        """Recursively animate solving the current maze. Try each direction in
        turn until a dead-end is reached, until a path is found to the end. Any
        dead-end paths are drawn as "undone". Effectively a depth-first search
        of the maze.

        Args:
            i (int): The X index of the current cell
            j (int): The Y index of the current cell

        Returns:
            bool: Whether this cell was on a successful path
        """
        current_cell = self._cells[i][j]
        current_cell.visited = True
        self._animate()
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        visitable_cells = self._get_visitable_cells(i, j, False)
        for _, vi, vj in visitable_cells:
            visitable_cell = self._cells[vi][vj]
            if visitable_cell.visited:
                continue
            current_cell.draw_move(visitable_cell)
            if self._solve_r(vi, vj):
                return True
            current_cell.draw_move(visitable_cell, True)

        return False
