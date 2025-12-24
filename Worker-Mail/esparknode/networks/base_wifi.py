from esparknode.utils.base_watchdog import BaseWatchdog


class BaseWiFiManager:
    def __init__(self, watchdog: BaseWatchdog, ssid: str, password: str):
        self.watchdog = watchdog
        self.ssid     = ssid
        self.password = password

    def ensure_wifi_on(self) -> bool:
        raise NotImplementedError('Subclasses must implement this method')

    def ensure_wifi_off(self) -> bool:
        raise NotImplementedError('Subclasses must implement this method')
