"""
Circle Shape Module.

This module provides the Circle class, a concrete implementation of the
Shape abstract base class. A Circle is defined by its radius and supports
area, perimeter, and description operations.

Classes:
    Circle: Represents a circle with a given radius.
"""

from .base_shape import Shape
from math import pi


class Circle(Shape):
    """A concrete shape class representing a circle.

    A circle is a round shape where all points on the boundary are
    equidistant from the center. This distance is called the radius.

    Attributes:
        radius (float): The radius of the circle.

    Methods:
        area(): Returns pi * radius^2.
        perimeter(): Returns 2 * pi * radius (circumference).
        describe(): Returns a formatted string with all circle details.
    """

    def __init__(self, radius):
        """Initialize a Circle with the given radius.

        Args:
            radius (float): The radius of the circle. Must be positive.

        """
        self.radius = radius

    def area(self):
        """Calculate the area of the circle.

        Returns:
            float: The area computed as pi * radius^2.

        """
        return pi * (self.radius ** 2)

    def perimeter(self):
        """Calculate the circumference (perimeter) of the circle.

        Returns:
            float: The circumference computed as 2 * pi * radius.

        """
        return pi * 2 * self.radius

    def describe(self):
        """Return a string description of the circle.

        Returns:
            str: A formatted string containing radius, area, and perimeter.
        """
        return f"Circle(radius = {self.radius}, area = {self.area():.2f}, perimeter = {self.perimeter():.2f})"

    def __str__(self):
        return "Circle(radius = {:.2f})".format(self.radius)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return super().__eq__(other)

    def __lt__(self, other):
        return super().__lt__(other)