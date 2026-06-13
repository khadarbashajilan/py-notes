class BankAccount:
    def __init__(self, account_number, balance):
        # Private attribute — set directly since account_number is read-only
        self._account_number = account_number
        
        # Uses the setter — validation runs automatically
        self.balance = balance

    # ---------- Read-Only Property ----------
    @property
    def account_number(self):
        """Returns the account number. Cannot be modified after creation."""
        return self._account_number
    # No setter defined — trying to assign raises AttributeError

    # ---------- Property with Getter and Setter ----------
    @property
    def balance(self):
        """Returns the current balance."""
        return self._balance

    @balance.setter
    def balance(self, amount):
        """Sets the balance after validating it's not negative."""
        if amount < 0:
            raise ValueError("Can't be negative")
        self._balance = amount
        print("Updated")

    # ---------- Computed Property (No Storage) ----------
    @property
    def is_overdrawn(self):
        """Returns True if balance is zero, False otherwise."""
        return self._balance == 0


# Create an account with zero balance
ba = BankAccount(123, 0)

# Read-only property — works fine
print(ba.account_number)  # 123

# Computed property — calculated on the fly
print(ba.is_overdrawn)    # True

# Would raise errors if uncommented:
# ba.account_number = 456  # AttributeError: can't set attribute
# ba.balance = -100        # ValueError: Can't be negative



class Student:
    def __init__(self, name, grade):
        # Read-only — set private variable directly (no setter exists)
        self._name = name

        # Uses the setter — validation runs automatically
        self.grade = grade

    # ---------- Read-Only Property ----------
    @property
    def name(self):
        """Returns student name. Cannot be modified."""
        return self._name

    # ---------- Property with Validation ----------
    @property
    def grade(self):
        """Returns the numeric grade."""
        return self._grade

    @grade.setter
    def grade(self, g):
        """Validates and sets the grade (0-100)."""
        if g < 0 or g > 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grade = g
        print("Updated")

    # ---------- Computed Property (NO SETTER, NO STORAGE) ----------
    @property
    def letter_grade(self):
        """Computes letter grade from numeric grade."""
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

    # ---------- Computed Property ----------
    @property
    def is_passing(self):
        """Returns True if grade is passing (≥60)."""
        return self._grade >= 60


class Rectangle:
    def __init__(self, width, height):
        # Uses the setter — validation runs automatically
        self.width = width
        self.height = height
    
    # ---------- Property with Getter and Setter ----------
    @property
    def width(self):
        """Returns the width of the rectangle."""
        return self._width
    
    @width.setter
    def width(self, w):
        """Sets the width after validating it's positive."""
        if w <= 0:
            raise ValueError("Width must be positive")
        self._width = w
    
    # ---------- Property with Getter and Setter ----------
    @property
    def height(self):
        """Returns the height of the rectangle."""
        return self._height
    
    @height.setter
    def height(self, h):
        """Sets the height after validating it's positive."""
        if h <= 0:
            raise ValueError("Height must be positive")
        self._height = h
    
    # ---------- Computed Property (No Storage) ----------
    @property
    def area(self):
        """Returns the area (width × height)."""
        return self._width * self._height
    
    # ---------- Computed Property (No Storage) ----------
    @property
    def perimeter(self):
        """Returns the perimeter 2 × (width + height)."""
        return 2 * (self._width + self._height)
    
    # ---------- Computed Property (No Storage) ----------
    @property
    def is_square(self):
        """Returns True if width equals height, False otherwise."""
        return self._width == self._height


# ---------- Testing ----------
r = Rectangle(10, 5)
print(r.width)       # 10
print(r.height)      # 5
print(r.area)        # 50
print(r.perimeter)   # 30
print(r.is_square)   # False

# Updates work with validation
r.width = 20
print(r.area)        # 100 — automatically recalculated!

# These would raise errors:
# r.width = -5       # ValueError: Width must be positive
# r.height = 0       # ValueError: Height must be positive
