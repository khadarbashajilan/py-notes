"""
Rectangle Shape Module.

This module provides the Rectangle class, a concrete implementation of the
Shape abstract base class. A Rectangle is defined by its length and width
and supports area, perimeter, and description operations.

Classes:
    Rectangle: Represents a rectangle with given length and width.
"""

from .base_shape import Shape


class Rectangle(Shape):
    """A concrete shape class representing a rectangle.

    A rectangle is a quadrilateral with four right angles. Opposite sides
    are equal in length.

    Attributes:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Methods:
        area(): Returns length * width.
        perimeter(): Returns 2 * (length + width).
        describe(): Returns a formatted string with all rectangle details.
    """

    def __init__(self, length, width):
        """Initialize a Rectangle with the given length and width.

        Args:
            length (float): The length of the rectangle. Must be positive.
            width (float): The width of the rectangle. Must be positive.
        """
        self.length = length
        self.width = width

    def area(self):
        """Calculate the area of the rectangle.

        Returns:
            float: The area computed as length * width.
        """
        return self.length * self.width

    def perimeter(self):
        """Calculate the perimeter of the rectangle.

        Returns:
            float: The perimeter computed as 2 * (length + width).
        """
        return (2 * self.length) + (2 * self.width)

    def describe(self):
        """Return a string description of the rectangle.

        Returns:
            str: A formatted string containing length, width, area, and perimeter.
        """
        return f"Rectangle(Length = {self.length}, Width = {self.width}, Area = {self.area()}, Perimeter = {self.perimeter()})"
