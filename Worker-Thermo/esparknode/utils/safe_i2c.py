# pylint: disable=import-error
from time import sleep_us

# pylint: disable=import-error
from machine import I2C, Pin


class SafeI2C:
    def __init__(self, id: int, scl: int, sda: int, freq: int = 400_000, timeout: int = 100_000):
        self.id      = id
        self.scl     = scl
        self.sda     = sda
        self.freq    = freq
        self.timeout = timeout

        self._i2c: I2C | None = None

    def init(self):
        if self._i2c is None:
            self._i2c = I2C(self.id, scl=Pin(self.scl), sda=Pin(self.sda), freq=self.freq, timeout=self.timeout)

    def deinit(self):
        if self._i2c is not None:
            scl = Pin(self.scl, Pin.OUT, Pin.OPEN_DRAIN, value=1)
            sda = Pin(self.sda, Pin.IN, Pin.OPEN_DRAIN)

            if sda.value() == 0:
                for _ in range(9):
                    scl.value(0)
                    sleep_us(10)
                    scl.value(1)
                    sleep_us(10)

                    if sda.value() == 1:
                        break

                sda_out = Pin(self.sda, Pin.OUT, Pin.OPEN_DRAIN, value=0)
                sleep_us(10)
                scl.value(1)
                sleep_us(10)
                sda_out.value(1)
                sleep_us(10)

            self._i2c = None

    def readfrom(self, addr: int, nbytes: int) -> bytes:
        self.init()

        return self._i2c.readfrom(addr, nbytes)

    def writeto(self, addr: int, data: bytes) -> None:
        self.init()

        self._i2c.writeto(addr, data)

    def writevto(self, addr: int, data: list[bytes]) -> None:
        self.init()

        self._i2c.writevto(addr, data)
