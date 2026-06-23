from abc import ABC, abstractmethod

class SmartDevice(ABC):
    def __init__(self):
        self.is_on=False

    @abstractmethod 
    def turn_on(self):
        self.is_on = True

    @abstractmethod 
    def turn_off(self):
        self.is_on = False

    def status(self):
        return f"Device is {"ON" if self.is_on else "OFF"}"
   
class LightBulb(SmartDevice):
    def __init__(self):
        super().__init__()
        self.brightness = 0

    def turn_off(self):
        self.is_on = False
        self.brightness = 0
        return "Light is Off"

    def turn_on(self):
        self.is_on = True
        self.brightness = 100
        return "Light is On"

class Fan(SmartDevice):
    def __init__(self):
        super().__init__()
        self.speed = 0

    def turn_on(self):
        self.speed = 100
        self.is_on = True
        return "Fan is On"     

    def turn_off(self):
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
