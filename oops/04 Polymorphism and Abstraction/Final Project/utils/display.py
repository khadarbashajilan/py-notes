"""Display utility for printing shape information."""


def print_all_info(shapes):
    """Print area and perimeter for each shape in the list."""
    for shape in shapes:
        print(f"{shape}: Area = {shape.area():.2f}, Perimeter = {shape.perimeter():.2f}")
