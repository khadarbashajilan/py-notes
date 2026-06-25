"""
Shape Logger Module.

This module provides the ShapeLogger class, a context manager that handles
logging shape data to a file. It ensures proper file handling by automatically
opening and closing the file, even if an exception occurs during logging.

The ShapeLogger implements the context manager protocol (__enter__ and __exit__)
to provide safe resource management using the 'with' statement.

Classes:
    ShapeLogger: A context manager for logging shape data to a file.
"""


class ShapeLogger:
    """A context manager for logging shape information to a file.

    This class implements the context manager protocol to safely open a log file,
    write shape data (area and perimeter), and guarantee the file is closed
    when the 'with' block exits — even if an exception is raised.

    Usage:
        with ShapeLogger('log.txt') as log:
            log.write(circle)
            log.write(square)

    Attributes:
        filename (str): The path to the log file.
        file (file object): The opened file handle (set during __enter__).
    """

    def __init__(self, filename='../log.txt'):
        """Initialize the ShapeLogger with a target filename.

        The file is not opened here — it is opened in __enter__ when
        the 'with' block starts.

        Args:
            filename (str): Path to the log file. Defaults to '../log.txt'.
        """
        self.filename = filename
        self.file = None

    def __enter__(self):
        """Open the log file and return the logger instance.

        This method is called when entering the 'with' block. It opens
        the file in append mode ('a') so existing log entries are preserved.

        Returns:
            ShapeLogger: The current instance (self) for use as the 'as' variable.
        """
        self.file = open(self.filename, 'a')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the log file when exiting the 'with' block.

        This method is called when exiting the 'with' block, whether
        normally or due to an exception. It ensures the file is always
        properly closed to prevent resource leaks.

        Args:
            exc_type: The exception type if an exception occurred, else None.
            exc_val: The exception value if an exception occurred, else None.
            exc_tb: The traceback if an exception occurred, else None.

        Returns:
            None (exceptions are not suppressed — they propagate after file close).
        """
        if self.file:
            self.file.close()

    def write(self, shape):
        """Log a shape's data to the open log file.

        Writes a formatted entry containing the shape's string representation,
        calculated area, and calculated perimeter.

        Args:
            shape (Shape): A Shape object with area() and perimeter() methods.

        Returns:
            None
        """
        if self.file:
            log_entry = f"{shape} | Area: {shape.area():.2f} | Perimeter: {shape.perimeter():.2f}\n"
            self.file.write(log_entry)
