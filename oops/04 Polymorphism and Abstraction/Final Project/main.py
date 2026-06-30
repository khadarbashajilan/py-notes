"""Shape Calculator — Entry point demonstrating OOP concepts."""

from shapes.circle import Circle
from shapes.square import Square
from shapes.rectangle import Rectangle
from shapes.triangle import Triangle
from utils.display import print_all_info
from utils.logger import ShapeLogger


def test_eq_and_sorting():
    """Test __eq__ and __lt__ methods."""
    print("\n--- Testing Equality & Sorting ---")
    c = Circle(5)
    s = Square(4)
    r = Rectangle(4, 4)
    t = Triangle(3, 4, 5, 5)
    others = [c, s, r, t]

    # Test __eq__: equal areas
    r_same = Rectangle(4, 4)
    print(f"r.area() = {r.area():.2f}, r_same.area() = {r_same.area():.2f}")
    print(f"r == r_same: {r == r_same}")

    # Test sorting by area
    print("\nShapes sorted by area:")
    for sh in sorted(others):
        print(f"  {sh}: Area = {sh.area():.2f}")

    return others


def main():
    """Run the shape calculator and tests."""
    c = Circle(5)
    s = Square(4)
    r = Rectangle(4, 4)
    t = Triangle(3, 4, 5, 5)
    shapes = [c, s, r, t]

    print("--- Shape Info ---")
    print_all_info(shapes)

    # Log to file
    with ShapeLogger('log.txt') as log:
        for shape in shapes:
            log.write(shape)

    # Run tests
    test_eq_and_sorting()


if __name__ == "__main__":
    main()
