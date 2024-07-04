from window import Window
from maze import Maze

_width = 800
_height = 600


def main():
    win = Window(_width, _height)

    maze = Maze(16, 16, 6, 6, 64, 64, win)

    maze._break_entrance_and_exit()

    maze._break_cells_r(0, 0)

    win.wait_for_close()


main()
