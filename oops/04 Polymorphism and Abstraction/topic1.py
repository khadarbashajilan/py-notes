class CarAlaram:
    def speak(self):
        return "Beep Beep !"

class Dog:
    def speak(self):
        return "Woof Woof!"

class Cat:
    def speak(self):
        return "Meow Meow!"

class SilentFish:
    def speak(self):
        return "~!"

def make_sound(everything):
    for thing in everything:
        print(thing.speak())

everything = [Dog(), Cat(), CarAlaram(), SilentFish()]
make_sound(everything)
