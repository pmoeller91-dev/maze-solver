from point import Point
from tkinter import Canvas


class Line:
    """A class representing a line on a canvas."""

    def __init__(self, p1: Point, p2: Point, width: int = 2) -> None:
        """Creates a new line with the given endpoints.

        Args:
            p1 (Point): The start point of the line
            p2 (Point): The end point of the line
            width (int): The width of the line, default 2
        """
        self.__p1 = p1
        self.__p2 = p2
        self.__width = width

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        """Draws the line using the given color on the provided canvas.

        Args:
            canvas (Canvas): The canvas the line will be drawn on
            fill_color (str): The color the line will be drawn in
        """
        p1, p2, width = self.__p1, self.__p2, self.__width
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=fill_color, width=width)
