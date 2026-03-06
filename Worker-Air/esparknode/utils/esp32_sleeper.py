# pylint: disable=import-error
from machine import deepsleep, lightsleep

from esparknode.utils.base_sleeper import BaseSleeper


class Sleeper(BaseSleeper):
    def light_sleep(self, duration: int) -> None:
        lightsleep(duration)

    def deep_sleep(self, duration: int) -> None:
        deepsleep(duration)
