"""
Shape Calculator — Main Entry Point.

This module demonstrates key OOP concepts including:
- Abstraction: Using the Shape abstract base class
- Polymorphism: Treating all shapes uniformly via the Shape interface
- Context Managers: Using ShapeLogger for safe file handling

The program creates various shape objects, displays their properties,
and logs the computed areas and perimeters to a file.

Usage:
    python main.py
"""

from shapes.circle import Circle
from shapes.square import Square
from utils.display import print_all_info
from utils.logger import ShapeLogger


def main():
    """Run the shape calculator demonstration.

    Creates a Circle and Square, displays their properties on the console,
    and logs their area and perimeter calculations to 'log.txt'.
    """
    # 1. Create shape instances
    c = Circle(5)
    s = Square(4)

    # 2. Store shapes in a list (polymorphic collection)
    my_shapes = [c, s]

    # 3. Display shape info using the polymorphic print utility
    print_all_info(my_shapes)

    # 4. Log shape data using the context manager
    with ShapeLogger('log.txt') as log:
        for shape in my_shapes:
            log.write(shape)


if __name__ == "__main__":
    main()
