class BankAccount:
    """Demonstrates read-only, validated, and computed properties."""

    def __init__(self, account_number, balance):
        """Initialize with a read-only account number and a validated balance."""
        self._account_number = account_number
        self.balance = balance  # Uses setter — validation runs automatically

    @property
    def account_number(self):
        """Return the read-only account number. No setter — cannot be modified."""
        return self._account_number

    @property
    def balance(self):
        """Return the current balance."""
        return self._balance

    @balance.setter
    def balance(self, amount):
        """Set the balance after validating it is not negative."""
        if amount < 0:
            raise ValueError("Can't be negative")
        self._balance = amount
        print("Updated")

    @property
    def is_overdrawn(self):
        """Return True if balance is exactly zero, else False."""
        return self._balance == 0


class Student:
    """Demonstrates read-only property, validated setter, and computed properties."""

    def __init__(self, name, grade):
        """Initialize with a read-only name and a validated numeric grade."""
        self._name = name
        self.grade = grade  # Uses setter — validation runs automatically

    @property
    def name(self):
        """Return the read-only student name. No setter — cannot be modified."""
        return self._name

    @property
    def grade(self):
        """Return the numeric grade."""
        return self._grade

    @grade.setter
    def grade(self, g):
        """Set the grade after validating it is between 0 and 100."""
        if g < 0 or g > 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grade = g
        print("Updated")

    @property
    def letter_grade(self):
        """Compute and return letter grade (A/B/C/D/F) from numeric grade."""
        if self._grade >= 90:
            return 'A'
        elif self._grade >= 80:
            return 'B'
        elif self._grade >= 70:
            return 'C'
        elif self._grade >= 60:
            return 'D'
        else:
            return 'F'

    @property
    def is_passing(self):
        """Return True if grade is 60 or above."""
        return self._grade >= 60


class Rectangle:
    """Demonstrates validated properties and computed properties (area, perimeter, is_square)."""

    def __init__(self, width, height):
        """Initialize rectangle with validated width and height."""
        self.width = width    # Uses setter — validation runs automatically
        self.height = height  # Uses setter — validation runs automatically

    @property
    def width(self):
        """Return the width."""
        return self._width

    @width.setter
    def width(self, w):
        """Set the width after validating it is positive."""
        if w <= 0:
            raise ValueError("Width must be positive")
        self._width = w

    @property
    def height(self):
        """Return the height."""
        return self._height

    @height.setter
    def height(self, h):
        """Set the height after validating it is positive."""
        if h <= 0:
            raise ValueError("Height must be positive")
        self._height = h

    @property
    def area(self):
        """Compute and return area (width × height)."""
        return self._width * self._height

    @property
    def perimeter(self):
        """Compute and return perimeter (2 × (width + height))."""
        return 2 * (self._width + self._height)

    @property
    def is_square(self):
        """Return True if width equals height."""
        return self._width == self._height


def main():
    """Test BankAccount, Student, and Rectangle property behavior."""

    # ---------- BankAccount Tests ----------
    print("=== BankAccount ===")
    ba = BankAccount(123, 0)
    assert ba.account_number == 123
    assert ba.is_overdrawn is True
    print("Test 1: Read-only account_number and computed is_overdrawn")

    ba.balance = 500
    assert ba.balance == 500
    assert ba.is_overdrawn is False
    print("Test 2: Balance update via setter")

    # ---------- Student Tests ----------
    print("\n=== Student ===")
    s = Student("Alice", 85)
    assert s.name == "Alice"
    assert s.grade == 85
    assert s.letter_grade == 'B'
    assert s.is_passing is True
    print("Test 3: Read-only name, validated grade, computed letter_grade and is_passing")

    # Test validation
    try:
        Student("Bob", -5)
        assert False
    except ValueError:
        print("Test 4: Negative grade rejected")

    try:
        Student("Bob", 150)
        assert False
    except ValueError:
        print("Test 5: Over-100 grade rejected")

    # ---------- Rectangle Tests ----------
    print("\n=== Rectangle ===")
    r = Rectangle(10, 5)
    assert r.width == 10
    assert r.height == 5
    assert r.area == 50
    assert r.perimeter == 30
    assert r.is_square is False
    print("Test 6: Valid rectangle with computed area, perimeter, is_square")

    r.width = 20
    assert r.area == 100
    print("Test 7: Width update auto-recalculates area")

    # Test validation
    try:
        Rectangle(-5, 10)
        assert False
    except ValueError:
        print("Test 8: Negative width rejected")

    try:
        Rectangle(5, 0)
        assert False
    except ValueError:
        print("Test 9: Zero height rejected")

    # Test square detection
    sq = Rectangle(7, 7)
    assert sq.is_square is True
    print("Test 10: Square correctly detected")

    print("\nAll tests passed!")


# ============================================================
# CONCEPT: Python @property Decorator
# ------------------------------------------------------------
# The @property decorator turns a method into a read-only
# attribute accessor, while @<name>.setter provides write
# access with built-in validation.
#
# Three property patterns demonstrated:
#   Read-only    — e.g., account_number, name (no setter).
#   Validated    — e.g., balance, grade, width, height
#                  (setter runs checks before assigning).
#   Computed     — e.g., is_overdrawn, letter_grade,
#                  is_passing, area, perimeter, is_square
#                  (derived from other attributes).
#
# This lets us keep a clean dot-access API while running
# logic under the hood.
# ============================================================

if __name__ == "__main__":
    main()
