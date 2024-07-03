from window import Window
from maze import Maze

_width = 800
_height = 600


def main():
    win = Window(_width, _height)

    maze = Maze(16, 16, 6, 6, 64, 64, win)

    win.wait_for_close()


main()
