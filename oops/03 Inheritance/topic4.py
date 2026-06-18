class Bird:
    def move(self):
        """Print a flying movement message."""
        print("Flying through the sky!")

    def lay_eggs(self):
        """Print an egg-laying message."""
        print("Laying eggs.")

class Fish:
    def move(self):
        """Print a swimming movement message."""
        print("Swimming in the water!")

    def has_scales(self):
        """Return whether this fish has scales."""
        return True

# Your task: create FlyingFish
class FlyingFish(Bird, Fish):
    # You don't need to add anything—it inherits everything!
    pass

# Test it
ff = FlyingFish()
ff.move()       # Which move() runs? Let's check MRO.
print(FlyingFish.__mro__)


"""
================================================================================
CONCEPT: MULTIPLE INHERITANCE & MRO (Method Resolution Order)
================================================================================

1. Multiple Inheritance:
   - A class can inherit from more than one parent class.
   - `FlyingFish(Bird, Fish)` inherits methods from both `Bird` and `Fish`.

2. MRO (Method Resolution Order):
   - Python uses the C3 linearization algorithm to determine which method to 
     call when a method name exists in multiple parents.
   - `FlyingFish.__mro__` shows the order: 
     `FlyingFish -> Bird -> Fish -> object`
   - Since `Bird` comes before `Fish` in the parent list, `Bird.move()` wins.

3. Diamond Problem Resolution:
   - Python's MRO handles the "diamond problem" (when two parents share a 
     common ancestor) predictably through the C3 linearization.

4. `__mro__` attribute:
   - Every class has a `__mro__` (or `mro()`) attribute that returns a tuple 
     of classes in the order Python will search for methods.

5. `pass` statement:
   - Used as a placeholder when a class inherits everything it needs and 
     doesn't add its own code.
================================================================================
"""
