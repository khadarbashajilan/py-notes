from abc import ABC, abstractmethod

class SmartDevice(ABC):
    def __init__(self):
        """Initialize the device in OFF state."""
        self.is_on=False

    @abstractmethod
    def turn_on(self):
        """Turn the device on. Must be implemented by subclasses."""
        self.is_on = True

    @abstractmethod
    def turn_off(self):
        """Turn the device off. Must be implemented by subclasses."""
        self.is_on = False

    def status(self):
        """Return a string showing whether the device is ON or OFF."""
        return f"Device is {"ON" if self.is_on else "OFF"}"

class LightBulb(SmartDevice):
    def __init__(self):
        """Initialize a LightBulb with brightness set to 0."""
        super().__init__()
        self.brightness = 0

    def turn_off(self):
        """Turn off the bulb and reset brightness to 0."""
        self.is_on = False
        self.brightness = 0
        return "Light is Off"

    def turn_on(self):
        """Turn on the bulb and set brightness to 100."""
        self.is_on = True
        self.brightness = 100
        return "Light is On"

class Fan(SmartDevice):
    def __init__(self):
        """Initialize a Fan with speed set to 0."""
        super().__init__()
        self.speed = 0

    def turn_on(self):
        """Turn on the fan and set speed to 100."""
        self.speed = 100
        self.is_on = True
        return "Fan is On"

    def turn_off(self):
        """Turn off the fan and reset speed to 0."""
        self.speed = 0
        self.is_on = False
        return "Fan is Off"

bulb = LightBulb()
fan = Fan()
print(bulb.status())
bulb.turn_on()
print(bulb.status())
print(fan.status())
fan.turn_on()
print(fan.status())


# ==========================================
# CONCEPT: ABSTRACT BASE CLASSES (ABC)
# ==========================================
#
# An Abstract Base Class (ABC) is a class that CANNOT be instantiated
# directly. It exists only to define a blueprint that subclasses must follow.
#
# ABC = SmartDevice
#   - Declares abstract methods: turn_on(), turn_off()
#   - Provides concrete methods: status()
#   - You CANNOT do: device = SmartDevice()  -> TypeError
#
# Subclasses = LightBulb, Fan
#   - MUST implement all abstract methods (turn_on, turn_off)
#   - CAN add their own methods and attributes
#   - INHERIT status() from the parent
#
# This enforces a CONTRACT: any subclass of SmartDevice MUST have
# turn_on() and turn_off() methods. Python raises an error if you
# try to create a subclass that forgets to implement them.
#
# ABSTRACTION = hiding complexity behind a simple interface.
# You don't need to know HOW a device turns on — just call turn_on().
