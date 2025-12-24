from time import sleep

from esparknode.actions.base_relay import BaseRelay
from esparknode.utils.esp32_gpio import GpioPin


class LatchingRelay(BaseRelay):
    def __init__(self, pin_set: int, pin_reset: int):
        self.pin_set   = pin_set
        self.pin_reset = pin_reset

    def turn_on(self):
        pin = GpioPin(self.pin_set)
        pin.set_high()
        sleep(0.5)
        pin.set_low()
        pin.deinit()

    def turn_off(self):
        pin = GpioPin(self.pin_reset)
        pin.set_high()
        sleep(0.5)
        pin.set_low()
        pin.deinit()
