# pylint: disable=import-error
from machine import ADC, Pin

from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.logging import log_debug

ADJUSTMENT_FACTOR: float = 1.04


class VoltageSensor(BaseSensor):
    def __init__(self, pin: int, voltage_full: float, voltage_empty: float, voltage_divider_ratio: float):
        self.pin                   = ADC(Pin(pin), atten=ADC.ATTN_0DB)
        self.voltage_full          = voltage_full
        self.voltage_empty         = voltage_empty
        self.voltage_divider_ratio = voltage_divider_ratio

    def _read_filtered(self, samples: int = 16, discard: int = 4) -> float:
        readings = [self.pin.read_uv() for _ in range(samples)]
        readings.sort()
        readings = readings[discard:-discard]

        return sum(readings) / len(readings)

    def _read(self) -> float:
        value = self._read_filtered() / 1_000_000 * self.voltage_divider_ratio * ADJUSTMENT_FACTOR
        log_debug(f'Voltage reading: {value:.3f} V')

        return value

    def read(self) -> dict:
        return {
            'battery' : max(0.0, min(100.0, ((self._read() - self.voltage_empty) / (self.voltage_full - self.voltage_empty)) * 100.0)),
        }
