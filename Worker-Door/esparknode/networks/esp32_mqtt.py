# pylint: disable=import-error
from time import sleep, time

from umqtt.simple import MQTTClient

from esparknode.configs import MQTT_KEEPALIVE, MQTT_TIMEOUT
from esparknode.constants import TOPIC_ACTION, TOPIC_DEVICE
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_error


class MQTTManager(BaseMQTTManager):
    def __init__(
            self,
            wifi_manager : BaseWiFiManager,
            watchdog     : BaseWatchdog,
            device_id    : str,
            host         : str,
            port         : int = 1883,
    ):
        super().__init__(wifi_manager, watchdog, device_id, host, port)

        self.client = MQTTClient(device_id, host, port, keepalive=MQTT_KEEPALIVE)

    def _ensure_mqtt(self):
        try:
            self.client.ping()

            return True
        # pylint: disable=broad-exception-caught
        except Exception:
            return self._connect_mqtt()

    def _connect_mqtt(self) -> bool:
        if not self.wifi_manager.ensure_wifi_on():
            return False

        deadline = time() + MQTT_TIMEOUT
        while time() < deadline:
            try:
                self.client.set_callback(self._mqtt_callback)
                self.client.connect()
                self.client.subscribe(f'{TOPIC_DEVICE}/{self.device_id}', qos=1)
                self.client.subscribe(f'{TOPIC_ACTION}/{self.device_id}', qos=1)

                return True
            # pylint: disable=broad-exception-caught
            except Exception as e:
                log_error(e, self.device_id, self)

                self.watchdog.feed()

                sleep(1)

        return False

    def publish(self, topic: str, msg: str, retain: bool = False) -> None:
        if not self._ensure_mqtt():
            return

        try:
            self.client.publish(topic, msg, qos=1, retain=retain)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            log_error(e, self.device_id, self)
