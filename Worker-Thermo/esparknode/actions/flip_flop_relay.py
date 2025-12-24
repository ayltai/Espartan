from time import sleep

from esparknode.actions.base_relay import BaseRelay
from esparknode.data.esp32_storage import Storage
from esparknode.utils.esp32_gpio import GpioPin

RELAY_STATE_KEY : str = 'relay_state'


class FlipFlopRelay(BaseRelay):
    def __init__(self, pin: int):
        self.pin     = pin
        self.storage = Storage()

    def turn_on(self):
        current_state = self.storage.get_int(RELAY_STATE_KEY)
        if current_state != 1:
            pin = GpioPin(self.pin)
            pin.set_high()
            sleep(0.5)
            pin.set_low()
            pin.deinit()

            self.storage.set_int(RELAY_STATE_KEY, 1)

    def turn_off(self):
        current_state = self.storage.get_int(RELAY_STATE_KEY)
        if current_state != 0:
            pin = GpioPin(self.pin)
            pin.set_high()
            sleep(0.5)
            pin.set_low()
            pin.deinit()

            self.storage.set_int(RELAY_STATE_KEY, 0)

    def toggle(self):
        current_state = self.storage.get_int(RELAY_STATE_KEY)
        if current_state == 1:
            self.turn_off()
        else:
            self.turn_on()

    def get_state(self) -> int:
        return self.storage.get_int(RELAY_STATE_KEY)
