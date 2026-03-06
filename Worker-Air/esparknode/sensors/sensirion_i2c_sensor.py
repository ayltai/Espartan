from struct import unpack

# pylint: disable=import-error
from machine import I2C

from esparknode.sensors.base_sensor import BaseSensor


class SensirionI2C(BaseSensor):
    def __init__(self, i2c: I2C, address: int):
        self.i2c     = i2c
        self.address = address

    @staticmethod
    def _calculate_crc(data: bytes) -> int:
        crc = 0xff

        for byte in data:
            crc ^= byte

            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1

                crc &= 0xff

        return crc & 0xff

    def _read_words(self, num_words: int) -> list:
        raw   = self.i2c.readfrom(self.address, num_words * 3)
        words = []

        for i in range(0, len(raw), 3):
            chunk = raw[i:i + 2]

            if self._calculate_crc(chunk) != raw[i + 2]:
                raise RuntimeError(f'CRC Mismatch at 0x{self.address:02x}')

            words.append(unpack('>H', chunk)[0])

        return words
