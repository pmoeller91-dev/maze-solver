from window import Window
from maze import Maze

_width = 800
_height = 600

# Setting smaller cells can result in stack overflows due to recursion limits
# and the recursive nature of the maze generation and solving. To avoid this,
# those algorithms would need to be converted to an iterative variant, or the
# recursion limit would need to be explicitly raised (which only sort of solves
# the issue).
_maze_padding = 4
_maze_cell_size = 32
_num_cols = (_width - _maze_padding * 2) // _maze_cell_size
_num_rows = (_height - _maze_padding * 2) // _maze_cell_size


def main():
    win = Window(_width, _height)

    maze = Maze(
        _maze_padding,
        _maze_padding,
        _num_rows,
        _num_cols,
        _maze_cell_size,
        _maze_cell_size,
        win,
    )
    maze.generate_maze()
    maze.solve()

    win.wait_for_close()


main()
