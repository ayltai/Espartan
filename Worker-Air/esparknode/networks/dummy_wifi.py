from esparknode.networks.base_wifi import BaseWiFiManager


class WiFiManager(BaseWiFiManager):
    def ensure_wifi_on(self) -> bool:
        return True

    def ensure_wifi_off(self) -> bool:
        return True
