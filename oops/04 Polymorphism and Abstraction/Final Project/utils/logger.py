"""Logger utility for writing shape data to a file."""


class ShapeLogger:
    """Context manager for logging shape data to a file."""

    def __init__(self, filename='log.txt'):
        """Initialize with the target filename."""
        self.filename = filename
        self.file = None

    def __enter__(self):
        """Open the log file for appending."""
        self.file = open(self.filename, 'a')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the log file."""
        if self.file:
            self.file.close()

    def write(self, shape):
        """Write a shape's area and perimeter to the log file."""
        if self.file:
            log_entry = f"{shape} | Area: {shape.area():.2f} | Perimeter: {shape.perimeter():.2f}\n"
            self.file.write(log_entry)
