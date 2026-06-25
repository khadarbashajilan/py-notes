
class Money:
    def __init__(self,amount, currency):
        """Store an amount and its currency (e.g., 100, 'USD')."""
        self.amount = amount
        self.currency = currency

    def __str__(self):
        """Return a readable string like Money(100, 'USD')."""
        return f"Money({self.amount}, '{self.currency}')"

    def same_currency(self,other):
        """Check if this Money and another Money use the same currency."""
        return self.currency == other.currency

    def __add__(self,other):
        """Add two Money objects of the same currency using the + operator."""
        if not isinstance(other,Money):
            raise TypeError("Not an Instace of Money")

        if not self.same_currency(other):
            raise ValueError(f"The Currency isnt same, got {other.currency} instead {self.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):
        """Check equality using == operator (amount and currency must match)."""
        if not isinstance(other, Money):
            raise TypeError("Not an Instace of Money")
        return self.amount == other.amount and self.currency == other.currency

    def __hash__(self):
        """Make Money hashable so it can be used in sets and dicts."""
        return hash((self.amount, self.currency))

    def __lt__(self,other):
        """Compare two Money objects using the < operator (same currency only)."""
        if not isinstance(other,Money):
            raise TypeError("Not an Instace of Money")

        if not self.same_currency(other):
            raise ValueError(f"The Currency isnt same, got {other.currency} instead {self.currency}")
        return other.amount > self.amount

    def __repr__(self) -> str:
        """Return a developer-friendly string like Money(100, USD)."""
        return f"Money({self.amount}, {self.currency})"



# ==========================================
# TEST CASES
# ==========================================

print("--- 1. Creation & Representation ---")
m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = Money(100, "EUR")

print(f"str(): {str(m1)}")   # Expected: Money(100, 'USD')
print(f"repr(): {repr(m1)}") # Expected: Money(100, USD)

print("\n--- 2. Equality (__eq__) ---")
m4 = Money(100, "USD")
print(f"100 USD == 100 USD: {m1 == m4}")  # Expected: True
print(f"100 USD == 50 USD:  {m1 == m2}")  # Expected: False
print(f"100 USD == 100 EUR: {m1 == m3}")  # Expected: False

print("\n--- 3. Hashing (__hash__) ---")
# Because you added __hash__, this will work perfectly!
wallet = {m1, m2, m4}  # m1 and m4 are duplicates, so one should be removed
print(f"Items in set (duplicates removed): {len(wallet)}") # Expected: 2

exchange_rates = {Money(1, "USD"): 1.0, Money(1, "EUR"): 1.09}
print(f"Dictionary lookup for EUR: {exchange_rates[Money(1, 'EUR')]}") # Expected: 1.09

print("\n--- 4. Addition (__add__) ---")
m_sum = m1 + m2
print(f"100 USD + 50 USD = {m_sum}") # Expected: Money(150, 'USD')

# Testing the ValueError for different currencies
try:
    m1 + m3
    print("❌ Failed: Should have raised a ValueError!")
except ValueError as e:
    print(f"✅ Caught Expected Error: {e}")

print("\n--- 5. Comparisons (__lt__) ---")
print(f"50 USD < 100 USD: {m2 < m1}") # Expected: True
print(f"100 USD < 50 USD: {m1 < m2}") # Expected: False

# Testing the ValueError for comparing different currencies
try:
    m1 < m3
    print("❌ Failed: Should have raised a ValueError!")
except ValueError as e:
    print(f"✅ Caught Expected Error: {e}")

print("\n--- 6. Type Checking ---")
# Testing the TypeError when interacting with non-Money objects
try:
    m1 == 100
    print("❌ Failed: Should have raised a TypeError!")
except TypeError as e:
    print(f"✅ Caught Expected Error: {e}")


# ==========================================
# CONCEPT: OPERATOR OVERLOADING (DUNDER METHODS)
# ==========================================
#
# Python lets you define custom behavior for built-in operators by
# implementing special "dunder" (double underscore) methods.
#
# DUNDER METHODS USED IN Money CLASS:
#   __init__  -> creates a new Money object
#   __str__   -> str(Money) -> readable string
#   __repr__  -> repr(Money) -> developer string
#   __add__   -> Money + Money -> adds amounts
#   __eq__    -> Money == Money -> checks equality
#   __lt__    -> Money < Money  -> compares amounts
#   __hash__  -> hash(Money)    -> allows use in sets/dicts
#
# WHY USE OPERATOR OVERLOADING?
#   Instead of m1.add(m2), you can write m1 + m2
#   Instead of m1.is_equal(m2), you can write m1 == m2
#   This makes custom classes feel like built-in types.
#
# TYPE SAFETY:
#   Each method checks if the other object is a Money instance.
#   If not, it raises TypeError. This prevents operations like:
#   Money(100, "USD") + 100  -> TypeError
#
# CURRENCY CHECK:
#   You can't add Money(100, "USD") + Money(50, "EUR")
#   The method raises ValueError to enforce business rules.
