class CarAlaram:
    def speak(self):
        """Return the sound a car alarm makes."""
        return "Beep Beep !"

class Dog:
    def speak(self):
        """Return the sound a dog makes."""
        return "Woof Woof!"

class Cat:
    def speak(self):
        """Return the sound a cat makes."""
        return "Meow Meow!"

class SilentFish:
    def speak(self):
        """Return the sound a silent fish makes."""
        return "~!"

def make_sound(everything):
    """Call speak() on each object in the list and print the result."""
    for thing in everything:
        print(thing.speak())

everything = [Dog(), Cat(), CarAlaram(), SilentFish()]
make_sound(everything)


# ==========================================
# CONCEPT: POLYMORPHISM
# ==========================================
#
# "Poly" means many, "morph" means forms. Polymorphism lets different
# objects share the same method name but behave differently.
#
# Here, Dog, Cat, CarAlaram, and SilentFish all have a speak() method.
# The make_sound() function doesn't care what type each object is — it
# just calls speak() on whatever it receives. Each class provides its
# own version of speak(), so the output changes depending on the object.
#
# This is RUNTIME POLYMORPHISM: Python decides which speak() to call
# at runtime based on the actual object type.
#
# DUCK TYPING: Python only cares that the object HAS a speak() method.
# It doesn't check the class type — "if it quacks like a duck, it's a duck."
