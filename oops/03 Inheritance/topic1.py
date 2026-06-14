class SmartDevice:
    def __init__(self, name):
        self.name = name
        self._status = 'OFF'

    def get_status(self):
        print(self._status)

    def turn_on(self):
        self._status = 'ON'

    def turn_off(self): 
        self._status = 'OFF'


class SmartLight(SmartDevice):
    def __init__(self, name):
        super().__init__(name)
        self._brightness = 50

    def get_status(self):
        super().get_status()
        print(self._brightness)

    def set_brightness(self, b):
        if not isinstance(b,(int,float)):
            raise TypeError("Type should be int or float")
        if b < 0 or b > 100:
            raise ValueError("Should need to be in between 1 and 100")
        self._brightness = b


class SmartThermostat(SmartDevice):
    def __init__(self,name):
        super().__init__(name)
        self._temperature = 22

    def get_status(self):
        super().get_status()
        print(self._temperature)

    def set_temperature(self, t):
        if not isinstance(t,(int,float)):
            raise TypeError("Type should be int or float")
        if t < 10 or t > 35:
            raise ValueError("Should need to be in between 10 and 35")
        self._temperature = t 
