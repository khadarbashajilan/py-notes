class TimeDuration:
    def __init__(self, hours, minutes):
        """Convert hours+minutes into total minutes, then store as hours and minutes."""
        # Convert everything to total minutes to handle rollovers automatically
        total_minutes = (hours * 60) + minutes

        # // is integer division (gets total hours)
        # % is modulo (gets the leftover minutes)
        self.hours = total_minutes // 60
        self.minutes = total_minutes % 60

    def __str__(self):
        """Return a readable string like TimeDuration(1HH : 40MM)."""
        # Added :02d so minutes format nicely (e.g., "05" instead of "5")
        return f"TimeDuration({self.hours}HH : {self.minutes:02d}MM)"

    def __repr__(self):
        """Return a developer-friendly string like TimeDuration(1, 40)."""
        return f"TimeDuration({self.hours}, {self.minutes})"

    @property
    def total_minutes(self):
        """Return the total duration converted to minutes (e.g., 1h 40m = 100)."""
        # A helpful shortcut for our math methods
        return (self.hours * 60) + self.minutes

    def __add__(self, other):
        """Add two TimeDuration objects using the + operator."""
        if not isinstance(other, TimeDuration):
            return NotImplemented

        return TimeDuration(self.hours + other.hours, self.minutes + other.minutes)

    def __sub__(self, other):
        """Subtract one TimeDuration from another using the - operator."""
        if not isinstance(other, TimeDuration):
            return NotImplemented

        diff_minutes = self.total_minutes - other.total_minutes

        return TimeDuration(0, diff_minutes)

    def __mul__(self, multiplier):
        """Multiply a TimeDuration by a number using the * operator."""
        # Multiplier should be a regular number, not a TimeDuration
        if not isinstance(multiplier, (int, float)):
            return NotImplemented

        return TimeDuration(0, int(self.total_minutes * multiplier))

    def __lt__(self, other):
        """Check if this TimeDuration is less than another using < operator."""
        if not isinstance(other, TimeDuration):
            return NotImplemented

        return self.total_minutes < other.total_minutes

    def __eq__(self, other):
        """Check if two TimeDurations are equal using == operator."""
        if not isinstance(other, TimeDuration):
            return NotImplemented

        return self.total_minutes == other.total_minutes

    def __hash__(self):
        """Make TimeDuration hashable so it can be used in sets and dicts."""
        return hash(self.total_minutes)

# ==========================================
# TEST CASES
# ==========================================

t1 = TimeDuration(1, 40)
t2 = TimeDuration(0, 30)

print(f"Addition: {t1} + {t2} = {t1 + t2}")
# Expected: TimeDuration(2HH : 10MM) (Notice how it rolled over!)

t3 = TimeDuration(2, 10)
t4 = TimeDuration(1, 40)
print(f"Subtraction: {t3} - {t4} = {t3 - t4}")
# Expected: TimeDuration(0HH : 30MM)

print(f"Multiplication: {t1} * 3 = {t1 * 3}")
# Expected: TimeDuration(5HH : 00MM)

print(f"Comparison: {t1} < {t3} is {t1 < t3}")
# Expected: True


# ==========================================
# CONCEPT: OPERATOR OVERLOADING FOR TIME
# ==========================================
#
# This class overloads operators for a TIME DURATION object.
# It lets you do math with time like you do with numbers.
#
# OPERATORS OVERLOADED:
#   +  (add)      -> TimeDuration + TimeDuration = combined time
#   -  (subtract) -> TimeDuration - TimeDuration = difference
#   *  (multiply) -> TimeDuration * 3 = 3x longer duration
#   <  (less than) -> compare which duration is shorter
#   == (equal)     -> check if two durations are the same
#
# INTERNAL TRICK: Everything is stored as total_minutes.
# This makes comparisons and math simple:
#   1 hour 40 minutes = 100 minutes
#   2 hours 10 minutes = 130 minutes
#   100 < 130 -> True (so 1h40m < 2h10m)
#
# ROLLOVER HANDLING:
#   TimeDuration(1, 90) -> internally becomes 2h 30m
#   Because 1*60 + 90 = 150 minutes -> 150 // 60 = 2 hours, 150 % 60 = 30 minutes
#
# NotImplemented:
#   When an unsupported type is used (e.g., TimeDuration + "hello"),
#   we return NotImplemented instead of raising an error. This lets
#   Python try the other object's method first (reflection).
