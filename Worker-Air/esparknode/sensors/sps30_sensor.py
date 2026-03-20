from struct import pack, unpack
from time import sleep, time

from esparknode.sensors.sensirion_i2c_sensor import SensirionI2C

STABILIZATION_DELAY : int = 30


class SPS30(SensirionI2C):
    def __init__(self, i2c, address: int = 0x69):
        super().__init__(i2c, address)

        self.is_started = False

    def start(self) -> None:
        sleep(1)

        self.i2c.writeto(self.address, b'\x00\x10\x03\x00\xac')

        self.is_started = True

        sleep(1)

    def stop(self) -> None:
        sleep(1)

        self.i2c.writeto(self.address, b'\x01\x04')

        self.is_started = False

        sleep(1)

    def housekeep(self) -> None:
        self.i2c.writeto(self.address, b'\x56\x07')

    def data_ready(self) -> bool:
        self.i2c.writeto(self.address, b'\x02\x02')
        words = self._read_words(1)

        return (words[0] & 0x01) == 0x01

    @staticmethod
    def _f(idx: int, words: list) -> float:
        return unpack('>f', pack('>HH', words[idx * 2], words[idx * 2 + 1]))[0]

    def read(self) -> dict:
        self.start()

        deadline = time() + STABILIZATION_DELAY
        while time() < deadline:
            sleep(1)

        results = {}

        while not self.data_ready():
            sleep(1)

        self.i2c.writeto(self.address, b'\x03\x00')
        words = self._read_words(20)

        results['pm1.0'] = self._f(0, words)
        results['pm2.5'] = self._f(1, words)
        results['pm4.0'] = self._f(2, words)
        results['pm10']  = self._f(3, words)

        self.stop()

        self.i2c.deinit()

        return results
