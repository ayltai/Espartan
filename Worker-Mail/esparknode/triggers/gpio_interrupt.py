# pylint: disable=import-error
from esp32 import wake_on_gpio, WAKEUP_ALL_LOW, WAKEUP_ANY_HIGH
from machine import Pin

from esparknode.triggers.base_trigger import BaseTrigger


class GpioInterrupt(BaseTrigger):
    def __init__(self, pins: list[int], pull: int = None, name: str = None):
        super().__init__('gpio_interrupt', name=name)

        self.pins = []

        for pin in pins:
            self.pins.append(Pin(pin, Pin.IN, pull=pull, hold=True))

    def start(self, pin_index: int = 0):
        self.pins[pin_index].irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._irq_handler)

    def stop(self, pin_index: int = 0):
        self.pins[pin_index].irq(handler=None)

    def wake_on(self, level: int = 0):
        wake_on_gpio(pins=self.pins, level=WAKEUP_ANY_HIGH if level == 1 else WAKEUP_ALL_LOW)

    def value(self, pin_index: int = 0) -> int:
        return self.pins[pin_index].value()

    def _irq_handler(self, pin: Pin):
        state = pin.value()

        for callback in self.callbacks:
            callback(True if state else False, self, self.pins.index(pin))
