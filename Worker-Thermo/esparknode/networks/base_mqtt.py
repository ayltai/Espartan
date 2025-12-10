from json import loads

from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.utils.base_watchdog import BaseWatchdog


class BaseMQTTManager:
    def __init__(
            self,
            wifi_manager : BaseWiFiManager,
            watchdog     : BaseWatchdog,
            device_id    : str,
            host         : str,
            port         : int = 1883,
    ):
        self.wifi_manager = wifi_manager
        self.watchdog     = watchdog
        self.host         = host
        self.port         = port
        self.device_id    = device_id
        self.on_callback  = None

    def set_on_callback(self, on_callback):
        self.on_callback = on_callback

    def _mqtt_callback(self, topic: bytes, msg: bytes):
        if self.on_callback:
            self.on_callback(topic.decode(), loads(msg.decode()))

    def _ensure_mqtt(self):
        raise NotImplementedError('Subclasses must implement this method')

    def _connect_mqtt(self) -> bool:
        raise NotImplementedError('Subclasses must implement this method')

    # pylint: disable=unused-argument
    def publish(self, topic: str, msg: str, retain: bool = False) -> None:
        raise NotImplementedError('Subclasses must implement this method')
