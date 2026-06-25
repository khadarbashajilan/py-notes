"""
Triangle Shape Module.

This module provides the Triangle class, a concrete implementation of the
Shape abstract base class. A Triangle is defined by its base, height, and
two side lengths, and supports area, perimeter, and description operations.

Classes:
    Triangle: Represents a triangle with given dimensions.
"""

from .base_shape import Shape


class Triangle(Shape):
    """A concrete shape class representing a triangle.

    A triangle is a polygon with three edges and three vertices.
    This implementation uses base and height for area calculation
    and three side lengths for perimeter calculation.

    Attributes:
        a (float): The length of side A.
        b (float): The length of side B (base).
        c (float): The length of side C.
        h (float): The height of the triangle (perpendicular to base).

    Methods:
        area(): Returns 0.5 * base * height.
        perimeter(): Returns the sum of all three sides.
        describe(): Returns a formatted string with all triangle details.
    """

    def __init__(self, base, height, side_a, side_c):
        """Initialize a Triangle with the given dimensions.

        Args:
            base (float): The base length of the triangle. Must be positive.
            height (float): The height perpendicular to the base. Must be positive.
            side_a (float): The length of side A. Must be positive.
            side_c (float): The length of side C. Must be positive.
        """
        self.a = side_a
        self.b = base
        self.c = side_c
        self.h = height

    def area(self):
        """Calculate the area of the triangle.

        Uses the formula: area = 0.5 * base * height.

        Returns:
            float: The area of the triangle.
        """
        return 0.5 * self.b * self.h

    def perimeter(self):
        """Calculate the perimeter of the triangle.

        Returns:
            float: The sum of all three side lengths.
        """
        return self.a + self.b + self.c

    def describe(self):
        """Return a string description of the triangle.

        Returns:
            str: A formatted string containing all sides, height, area, and perimeter.
        """
        return f"Triangle(Side A = {self.a}, Side B = {self.b}, Side C = {self.c}, Height = {self.h}, Area = {self.area()}, Perimeter = {self.perimeter()})"



