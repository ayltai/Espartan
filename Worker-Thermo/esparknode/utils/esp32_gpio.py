# pylint: disable=import-error
from machine import Pin


class GpioPin:
    def __init__(self, pin: int, initial_state: int = None):
        self.pin = Pin(pin, Pin.OUT, value=initial_state)

    def set_high(self):
        self.pin.value(1)

    def set_low(self):
        self.pin.value(0)
