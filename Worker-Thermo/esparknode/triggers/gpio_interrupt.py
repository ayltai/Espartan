# pylint: disable=import-error
from esp32 import wake_on_gpio, WAKEUP_ALL_LOW, WAKEUP_ANY_HIGH
from machine import Pin

from esparknode.triggers.base_trigger import BaseTrigger


class GpioInterrupt(BaseTrigger):
    def __init__(self, pin: int, pull: int = None, name: str = None):
        super().__init__('gpio_interrupt', name=name)

        self.pin = Pin(pin, Pin.IN, pull)

    def get_value(self):
        return self.pin.value()

    def start(self):
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._irq_handler)

    def stop(self):
        self.pin.irq(handler=None)

    def wake_on(self, level: int = 0):
        wake_on_gpio(pins=[self.pin], level=WAKEUP_ANY_HIGH if level else WAKEUP_ALL_LOW)

    def value(self):
        return self.pin.value()

    def _irq_handler(self, pin: Pin):
        state = pin.value()

        for callback in self.callbacks:
            callback(True if state else False, self)
