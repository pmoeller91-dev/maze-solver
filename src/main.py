from window import Window
from line import Line
from point import Point


def main():
    win = Window(800, 600)

    # A simple "X" through the whole canvas
    line = Line(Point(0, 0), Point(800, 600))
    line2 = Line(Point(800, 0), Point(0, 600))

    win.draw_line(line, fill_color="black")
    win.draw_line(line2, fill_color="black")

    win.wait_for_close()


main()
