"""
Abstract Base Shape Module.

This module defines the Shape abstract base class (ABC) that serves as the
foundation for all geometric shape implementations. Any concrete shape class
must implement the area(), perimeter(), and describe() methods.

Classes:
    Shape: Abstract base class for all geometric shapes.
"""

from abc import abstractmethod, ABC


class Shape(ABC):
    """Abstract base class representing a geometric shape.

    All concrete shape classes (Circle, Square, Rectangle, Triangle)
    must inherit from this class and implement the three abstract methods:
    area(), perimeter(), and describe().

    This enforces a consistent interface across all shape types,
    enabling polymorphic usage throughout the application.
    """

    @abstractmethod
    def area(self):
        """Calculate and return the area of the shape.

        Returns:
            float: The computed area of the shape.
        """
        pass

    @abstractmethod
    def perimeter(self):
        """Calculate and return the perimeter of the shape.

        Returns:
            float: The computed perimeter (total boundary length) of the shape.
        """
        pass

    @abstractmethod
    def describe(self):
        """Return a string description of the shape.

        The description includes the shape type, its dimensions, area, and perimeter in a human-readable format.

        Returns:
            str: A formatted string describing the shape and its properties.
        """
        pass

    # ------------------------------------------------------------------
    #  Rich comparison helpers
    # ------------------------------------------------------------------
    def __eq__(self, other):
        """Two shapes are equal if they have the same area (regardless of type).

        Args:
            other: Another Shape instance to compare against.

        Returns:
            bool: True if areas match (within floating-point tolerance), else False.
        """
        if not isinstance(other, Shape):
            return NotImplemented
        return abs(self.area() - other.area()) < 1e-9

    def __lt__(self, other):
        """Compare shapes by area for sorting.

        Args:
            other: Another Shape instance to compare against.

        Returns:
            bool: True if this shape's area is less than the other's area.
        """
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()
