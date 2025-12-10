# pylint: disable=import-error
from machine import I2C, Pin

from esparknode.libraries import SHT20
from esparknode.sensors.base_sensor import BaseSensor


class SHT20Sensor(BaseSensor):
    def __init__(self, scl_pin: int, sda_pin: int):
        self.sensor = SHT20(I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin)))

    def read(self) -> dict:
        results = {}

        try:
            results['temperature'] = self.sensor.temperature
        except OSError:
            pass

        try:
            results['humidity'] = self.sensor.humidity
        except OSError:
            pass

        return results
