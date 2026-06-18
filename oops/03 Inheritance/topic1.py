class SmartDevice:
    def __init__(self, name):
        """Initialize a smart device with a name and default status OFF."""
        self.name = name
        self._status = 'OFF'

    def get_status(self):
        """Print the current status of the device."""
        print(self._status)

    def turn_on(self):
        """Turn the device ON by setting status to 'ON'."""
        self._status = 'ON'

    def turn_off(self): 
        """Turn the device OFF by setting status to 'OFF'."""
        self._status = 'OFF'


class SmartLight(SmartDevice):
    def __init__(self, name):
        """Initialize a smart light with default brightness 50."""
        super().__init__(name)
        self._brightness = 50

    def get_status(self):
        """Print device status and current brightness level."""
        super().get_status()
        print(self._brightness)

    def set_brightness(self, b):
        """Set brightness level (0-100). Validates type and range."""
        if not isinstance(b,(int,float)):
            raise TypeError("Type should be int or float")
        if b < 0 or b > 100:
            raise ValueError("Should need to be in between 1 and 100")
        self._brightness = b


class SmartThermostat(SmartDevice):
    def __init__(self,name):
        """Initialize a smart thermostat with default temperature 22."""
        super().__init__(name)
        self._temperature = 22

    def get_status(self):
        """Print device status and current temperature."""
        super().get_status()
        print(self._temperature)

    def set_temperature(self, t):
        """Set temperature (10-35°C). Validates type and range."""
        if not isinstance(t,(int,float)):
            raise TypeError("Type should be int or float")
        if t < 10 or t > 35:
            raise ValueError("Should need to be in between 10 and 35")
        self._temperature = t


"""
================================================================================
CONCEPT: SINGLE INHERITANCE & METHOD OVERRIDING
================================================================================

1. Inheritance (Single):
   - A class (child/derived) inherits attributes and methods from one parent class.
   - `SmartLight(SmartDevice)` and `SmartThermostat(SmartDevice)` inherit from 
     `SmartDevice`, gaining `name`, `_status`, `turn_on()`, and `turn_off()`.

2. super():
   - Used to call the parent class constructor or methods from the child class.
   - `super().__init__(name)` in child classes calls `SmartDevice.__init__`.
   - `super().get_status()` reuses the parent's status-printing logic.

3. Method Overriding:
   - Child classes redefine a method inherited from the parent.
   - `get_status()` is overridden in both `SmartLight` and `SmartThermostat` 
     to extend the parent's behavior with subclass-specific info.

4. Encapsulation via Name Mangling Convention:
   - The underscore prefix `_status`, `_brightness`, `_temperature` signals 
     these attributes are intended for internal use (protected convention).

5. Validation:
   - `set_brightness()` and `set_temperature()` validate input types and range,
     raising `TypeError` or `ValueError` for invalid inputs.
================================================================================
"""
