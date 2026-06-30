"""Circle shape implementation."""

from .base_shape import Shape
from math import pi


class Circle(Shape):
    """A circle defined by its radius."""

    def __init__(self, radius):
        """Initialize a Circle with the given radius."""
        self.radius = radius

    def area(self):
        """Return the area (πr²)."""
        return pi * (self.radius ** 2)

    def perimeter(self):
        """Return the perimeter (circumference, 2πr)."""
        return 2 * pi * self.radius

    def describe(self):
        """Return a formatted description with dimensions, area, and perimeter."""
        return str(self)

    def __str__(self):
        return "Circle(radius = {:.2f})".format(self.radius)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __lt__(self, other):
        return super().__lt__(other)
