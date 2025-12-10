# pylint: disable=import-error
from machine import Pin


class GpioPin:
    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.OUT)

    def set_high(self):
        self.pin.value(1)

    def set_low(self):
        self.pin.value(0)
