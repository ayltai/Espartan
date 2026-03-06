from struct import pack
from time import sleep

# pylint: disable=import-error
from machine import I2C

from esparknode.sensors.sensirion_i2c_sensor import SensirionI2C

TARGET_CO2: int = 400


class SCD4X(SensirionI2C):
    def __init__(self, i2c: I2C, address: int = 0x62):
        super().__init__(i2c, address)

        self.is_started = False

        self.stop()

    def configure_altitude(self, altitude: int) -> None:
        self.i2c.writeto(self.address, b'\x24\x27' + altitude.to_bytes(2, 'big') + bytes([self._calculate_crc(altitude.to_bytes(2, 'big'))]))

        sleep(1)

    def start(self):
        sleep(1)

        self.i2c.writeto(self.address, b'\x21\xb1')

        self.is_started = True

    def stop(self):
        self.i2c.writeto(self.address, b'\x3f\x86')

        self.is_started = False

    def housekeep(self) -> None:
        is_started = self.is_started

        if self.is_started:
            self.stop()

            sleep(1)

        word = pack('>H', TARGET_CO2)
        data = b'\x36\x2f' + word + bytes([self._calculate_crc(word)])

        self.i2c.writeto(self.address, data)

        sleep(1)

        if is_started:
            self.start()

    def read(self) -> dict:
        results = {}

        while True:
            self.i2c.writeto(self.address, b'\xe4\x2f')
            sleep(0.1)

            status = self.i2c.readfrom(self.address, 3)
            if (status[0] & 0x07 or status[1]) != 0:
                break

            sleep(1)

        self.i2c.writeto(self.address, b'\xec\x05')
        words = self._read_words(3)

        co2         = int(words[0])
        temperature = -45.0 + 175.0 * words[1] / 65536.0
        humidity    = 100.0 * words[2] / 65536.0

        results['co2']         = co2
        results['temperature'] = temperature
        results['humidity']    = humidity

        return results
