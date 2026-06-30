"""Abstract base class for geometric shapes."""

from abc import abstractmethod, ABC


class Shape(ABC):
    """Abstract base for all shapes."""

    @abstractmethod
    def area(self):
        """Return the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self):
        """Return the perimeter of the shape."""
        pass

    @abstractmethod
    def describe(self):
        """Return a string description of the shape."""
        pass

    def __eq__(self, other):
        """Check equality based on area (within floating-point tolerance)."""
        if not isinstance(other, Shape):
            return NotImplemented
        return abs(self.area() - other.area()) < 1e-9

    def __lt__(self, other):
        """Compare shapes by area for sorting."""
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()
