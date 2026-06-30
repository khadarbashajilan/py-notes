"""Rectangle shape implementation."""

from .base_shape import Shape


class Rectangle(Shape):
    """A rectangle defined by its length and width."""

    def __init__(self, length, width):
        """Initialize a Rectangle with the given length and width."""
        self.length = length
        self.width = width

    def area(self):
        """Return the area (length * width)."""
        return self.length * self.width

    def perimeter(self):
        """Return the perimeter (2 * (length + width))."""
        return 2 * (self.length + self.width)

    def describe(self):
        """Return a formatted description with dimensions, area, and perimeter."""
        return str(self)

    def __str__(self):
        return "Rectangle(length = {:.2f}, width = {:.2f})".format(self.length, self.width)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __lt__(self, other):
        return super().__lt__(other)
