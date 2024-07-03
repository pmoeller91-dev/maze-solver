from window import Window
from cell import Cell

_width = 800
_height = 600


def main():
    win = Window(_width, _height)

    cells = []
    for i in range(16):
        row = ((i * 2) // (_width // 64)) * 2
        col = (i * 2) % (_width // 64)
        cell = Cell(win, bool(i & 1), bool(i & 2), bool(i & 4), bool(i & 8))
        cells.append(cell)
        cell.draw(16 + col * 64, 16 + row * 64, 16 + 64 + col * 64, 16 + 64 + row * 64)

    win.wait_for_close()


main()
