# pylint: disable=import-error
from network import STA_IF, WLAN
# pylint: disable=wrong-import-order
from time import sleep

from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug

TIMEOUT: int = 20


class WiFiManager(BaseWiFiManager):
    def __init__(self, watchdog: BaseWatchdog, ssid: str, password: str) -> None:
        super().__init__(watchdog, ssid, password)

        self.wlan = WLAN(STA_IF)

    def ensure_wifi_on(self) -> bool:
        self.wlan.active(True)

        if not self.wlan.isconnected():
            log_debug(f'Connecting to WiFi SSID: {self.ssid}')
            self.wlan.connect(self.ssid, self.password)

            timeout: int = 0
            while not self.wlan.isconnected() and timeout < TIMEOUT:
                self.watchdog.feed()

                sleep(1)

                timeout += 1

        log_debug(f'WiFi connected: {self.wlan.ifconfig()}')
        return self.wlan.isconnected()

    def ensure_wifi_off(self) -> bool:
        self.wlan.active(False)
        log_debug('WiFi turned off')

        return not self.wlan.isconnected()
