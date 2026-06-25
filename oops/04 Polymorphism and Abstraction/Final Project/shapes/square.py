"""
Square Shape Module.

This module provides the Square class, a concrete implementation of the
Shape abstract base class. A Square is defined by its side length and
supports area, perimeter, and description operations.

Classes:
    Square: Represents a square with a given side length.
"""

from .base_shape import Shape


class Square(Shape):
    """A concrete shape class representing a square.

    A square is a quadrilateral with four equal sides and four right angles.

    Attributes:
        side (float): The length of one side of the square.

    Methods:
        area(): Returns side^2.
        perimeter(): Returns 4 * side.
        describe(): Returns a formatted string with all square details.
    """

    def __init__(self, side):
        """Initialize a Square with the given side length.

        Args:
            side (float): The length of each side. Must be positive.
        """
        self.side = side

    def area(self):
        """Calculate the area of the square.

        Returns:
            float: The area computed as side^2.
        """
        return self.side ** 2

    def perimeter(self):
        """Calculate the perimeter of the square.

        Returns:
            float: The perimeter computed as 4 * side.
        """
        return 4 * self.side

    def describe(self):
        """Return a string description of the square.

        Returns:
            str: A formatted string containing side, area, and perimeter.
        """
        return f"Square(Side = {self.side}, Area = {self.area()}, Perimeter = {self.perimeter()})"


