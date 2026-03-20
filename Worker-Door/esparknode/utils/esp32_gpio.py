# pylint: disable=import-error
from machine import Pin


class GpioPin:
    def __init__(self, pin: int, hold: bool = False):
        self.pin  = pin
        self.hold = hold

    def set_high(self):
        Pin(self.pin, Pin.OUT, value=1, hold=self.hold)

    def set_low(self):
        Pin(self.pin, Pin.OUT, value=0, hold=self.hold)

    def deinit(self):
        Pin(self.pin, Pin.IN, pull=None)
