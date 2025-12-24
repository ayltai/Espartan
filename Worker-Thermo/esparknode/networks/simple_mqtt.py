from paho.mqtt.client import Client

from esparknode.configs import MQTT_KEEPALIVE
from esparknode.constants import TOPIC_ACTION, TOPIC_DEVICE, TOPIC_OTA
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug


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

        self.client = Client(client_id=device_id, clean_session=False, reconnect_on_failure=True)

    # pylint: disable=unused-argument
    def _on_message(self, client, userdata, message):
        log_debug(f'MQTT Message Received: Topic={message.topic}, Payload={message.payload}')

        self._mqtt_callback(message.topic.encode(), message.payload)

    def _ensure_mqtt(self):
        if self.client.is_connected():
            log_debug('MQTT already connected')

            return True

        return self._connect_mqtt()

    def _connect_mqtt(self) -> bool:
        log_debug('Connecting to MQTT broker...')

        self.client.connect(self.host, self.port, keepalive=MQTT_KEEPALIVE)

        self.client.on_message = self._on_message

        self.client.subscribe(f'{TOPIC_DEVICE}/{self.device_id}', qos=1)
        self.client.subscribe(f'{TOPIC_ACTION}/{self.device_id}', qos=1)
        self.client.subscribe(f'{TOPIC_OTA}/{self.device_id}', qos=1)

        self.client.loop_start()

        return True

    def publish(self, topic: str, msg: str, retain: bool = False) -> None:
        if not self._ensure_mqtt():
            return

        self.client.publish(topic, msg, qos=1, retain=retain)
