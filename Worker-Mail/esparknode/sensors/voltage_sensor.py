# pylint: disable=import-error
from machine import ADC, Pin
from time import sleep_ms

from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.logging import log_debug


class VoltageSensor(BaseSensor):
    def __init__(self, pin: int, voltage_full: float, voltage_empty: float, voltage_divider_ratio: float):
        self.pin                   = ADC(Pin(pin), atten=ADC.ATTN_0DB)
        self.voltage_full          = voltage_full
        self.voltage_empty         = voltage_empty
        self.voltage_divider_ratio = voltage_divider_ratio

    def _read_filtered(self, samples: int = 16, discard: int = 4) -> float:
        readings = []

        for i in range(samples):
            reading = self.pin.read_uv()
            if reading > 0:
                readings.append(reading)

            if i % 4 == 0:
                sleep_ms(0)

        readings.sort()

        if len(readings) > (discard * 2):
            readings = readings[discard:-discard]

        return sum(readings) / len(readings)

    def _read(self) -> float:
        value = self._read_filtered() / 1_000_000 * self.voltage_divider_ratio
        log_debug(f'Voltage reading: {value:.3f} V')

        return value

    def read(self) -> dict:
        return {
            'battery' : max(0.0, min(100.0, ((self._read() - self.voltage_empty) / (self.voltage_full - self.voltage_empty)) * 100.0)),
        }
