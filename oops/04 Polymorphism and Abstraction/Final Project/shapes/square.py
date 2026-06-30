"""Square shape implementation."""

from .base_shape import Shape


class Square(Shape):
    """A square defined by its side length."""

    def __init__(self, side):
        """Initialize a Square with the given side length."""
        self.side = side

    def area(self):
        """Return the area (side²)."""
        return self.side ** 2

    def perimeter(self):
        """Return the perimeter (4 * side)."""
        return 4 * self.side

    def describe(self):
        """Return a formatted description with dimensions, area, and perimeter."""
        return str(self)

    def __str__(self):
        return "Square(side = {:.2f})".format(self.side)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __lt__(self, other):
        return super().__lt__(other)
