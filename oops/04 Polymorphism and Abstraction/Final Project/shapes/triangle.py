"""Triangle shape implementation."""

from .base_shape import Shape


class Triangle(Shape):
    """A triangle defined by its base, height, and two other side lengths."""

    def __init__(self, base, height, side_a, side_c):
        """Initialize a Triangle with the given dimensions."""
        self.base = base
        self.height = height
        self.side_a = side_a
        self.side_c = side_c

    def area(self):
        """Return the area (0.5 * base * height)."""
        return 0.5 * self.base * self.height

    def perimeter(self):
        """Return the perimeter (sum of all three sides)."""
        return self.side_a + self.base + self.side_c

    def describe(self):
        """Return a formatted description with dimensions, area, and perimeter."""
        return str(self)

    def __str__(self):
        return "Triangle(base = {:.2f}, height = {:.2f})".format(self.base, self.height)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __lt__(self, other):
        return super().__lt__(other)
