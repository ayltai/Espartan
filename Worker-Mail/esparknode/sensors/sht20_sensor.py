# pylint: disable=import-error
from machine import I2C, Pin

from esparknode.libraries import SHT20
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.logging import log_error

class SHT20Sensor(BaseSensor):
    def __init__(self, scl_pin: int, sda_pin: int):
        self.sensor = SHT20(I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=100_000))

    def read(self) -> dict:
        results = {}

        try:
            results['temperature'] = self.sensor.temperature
        except OSError as e:
            log_error(e)

        try:
            results['humidity'] = self.sensor.humidity
        except OSError as e:
            log_error(e)

        return results
