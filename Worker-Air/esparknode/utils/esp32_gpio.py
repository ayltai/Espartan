# pylint: disable=import-error
from machine import Pin


class GpioPin:
    def __init__(self, pin: int):
        self.pin = pin

    def set_high(self):
        Pin(self.pin, Pin.OUT, value=1)

    def set_low(self):
        Pin(self.pin, Pin.OUT, value=0)

    def deinit(self):
        Pin(self.pin, Pin.IN, pull=None)
