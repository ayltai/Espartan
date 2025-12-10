# pylint: disable=import-error
from machine import WDT

from esparknode.configs import WATCHDOG_ENABLED, WATCHDOG_TIMEOUT
from esparknode.utils.base_watchdog import BaseWatchdog

# pylint: disable=invalid-name
watchdog : WDT | None = None


class Watchdog(BaseWatchdog):
    def __init__(self) -> None:
        global watchdog
        if WATCHDOG_ENABLED and watchdog is None:
            watchdog = WDT(timeout=WATCHDOG_TIMEOUT)

    def feed(self) -> None:
        global watchdog
        if watchdog is not None:
            watchdog.feed()
