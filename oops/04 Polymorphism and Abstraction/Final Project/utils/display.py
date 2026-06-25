"""
Display Utility Module.

This module provides utility functions for displaying shape information
to the console. It leverages polymorphism by calling the describe() method
on any Shape object, regardless of its concrete type.

Functions:
    print_all_info(shapes): Prints descriptions of all shapes in a list.
"""


def print_all_info(shapes):
    """Print the description of each shape in the given list.

    This function iterates through a list of Shape objects and prints
    their describe() output. It works with any shape type due to
    polymorphism — each shape provides its own describe() implementation.

    Args:
        shapes (list): A list of Shape objects (Circle, Square, Rectangle, Triangle, etc.).

    Returns:
        None
    """
    for shape in shapes:
        print(shape.describe())
