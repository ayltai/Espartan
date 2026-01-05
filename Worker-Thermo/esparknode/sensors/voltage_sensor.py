# pylint: disable=import-error
from machine import ADC, Pin

from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.logging import log_debug

GPIO_VOLTAGE : float = 3.3
RESOLUTION   : float = 65535.0


class VoltageSensor(BaseSensor):
    def __init__(self, pin: int, voltage_full: float, voltage_empty: float, voltage_divider_ratio: float):
        self.pin                   = ADC(Pin(pin), atten=ADC.ATTN_11DB)
        self.voltage_full          = voltage_full
        self.voltage_empty         = voltage_empty
        self.voltage_divider_ratio = voltage_divider_ratio

    def _read(self) -> float:
        value = (self.pin.read_u16() / RESOLUTION) * GPIO_VOLTAGE * self.voltage_divider_ratio
        log_debug(f'Voltage reading: {value:.2f} V')

        return value

    def read(self) -> dict:
        return {
            'battery' : max(0.0, min(100.0, ((self._read() - self.voltage_empty) / (self.voltage_full - self.voltage_empty)) * 100.0)),
        }
