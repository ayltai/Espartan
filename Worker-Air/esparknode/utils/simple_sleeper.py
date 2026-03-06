from sys import exit
from time import sleep

from esparknode.utils.base_sleeper import BaseSleeper


class Sleeper(BaseSleeper):
    def light_sleep(self, duration: int) -> None:
        sleep(duration / 1000)

    def deep_sleep(self, duration: int) -> None:
        exit(0)
