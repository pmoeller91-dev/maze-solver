from typing_extensions import Self


class Point:
    """Represents a single point on a canvas.

    Attributes:
        x (int): The X coordinate of the point.
        y (int): The Y coordinate of the point.
    """

    def __init__(self, x: int, y: int) -> None:
        """Creates a new point object with the given coordinates.

        Args:
            x (int): The initial X coordinate of the point.
            y (int): The initial Y coordinate of the point.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Return a representation of the point

        Returns:
            str: String representing the point.
        """
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """Return a string representing the point. Same as ``__repr__``.

        Returns:
            str: String representing the point.
        """
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        """Compares two ``Point``s for equality. Returns true if x and y match.
        Returns NotImplemented if ``other`` is not a ``Point``.

        Args:
            other (object): The object being compared.

        Returns:
            bool: True if Points are equal, False otherwise. NotImplemented if
            ``other`` is not a ``Point``.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Self:
        """Returns the inverse of the point, with x and y inverted.

        Returns:
            Self: A point with inverted coordintaes
        """
        return Point(x=-(self.x), y=-(self.y))

    def __add__(self, other: object) -> Self:
        """Adds two points, returning a new point. Returns NotImplemented if
        ``other`` is not a ``Point``.

        Args:
            other (object): The object being added

        Returns:
            Self: A point with the x and y equal to the sum of the coordinates
            of the two points.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: object) -> Self:
        """Subtracts two points, returning a new point. Returns NotImplemented
        if ``other`` is not a ``Point``.

        Args:
            other (object): The object being subtracted

        Returns:
            Self: A point with the x and y equal to the difference of the coordinates
            of the two points.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return Point(x=self.x - other.x, y=self.y - other.y)
    
    def __rsub__(self, other: object) -> Self:
        """Subtracts two points, returning a new point. Returns NotImplemented
        if ``other`` is not a ``Point``.

        Args:
            other (object): The object being subtracted

        Returns:
            Self: A point with the x and y equal to the difference of the coordinates
            of the two points.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return Point(x=other.x - self.x, y=other.y - self.y)