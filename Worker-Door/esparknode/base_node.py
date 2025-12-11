from json import dumps
from time import sleep, time

from esparknode.configs import CAPABILITIES, ENVIRONMENT, PARAMETERS_UPDATE_TIMEOUT, UNUSED_PINS
from esparknode.constants import NODE_NAME, NODE_VERSION, TOPIC_ACTION, TOPIC_DEVICE, TOPIC_OTP, TOPIC_REGISTRATION
from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug


class BaseNode:
    def __init__(
            self,
            device_id         : str,
            sleeper           : BaseSleeper,
            watchdog          : BaseWatchdog,
            wifi_manager      : BaseWiFiManager,
            mqtt_manager      : BaseMQTTManager,
            bluetooth_manager : BaseBluetoothManager = None,
            sensors           : list[BaseSensor]     = None,
            triggers          : list[BaseTrigger]    = None,
    ):
        self.device_id         = device_id
        self.sleeper           = sleeper
        self.watchdog          = watchdog
        self.wifi_manager      = wifi_manager
        self.mqtt_manager      = mqtt_manager
        self.bluetooth_manager = bluetooth_manager
        self.sensors           = sensors if sensors is not None else []
        self.triggers          = triggers if triggers is not None else []

        self.parameters_updated : bool = False
        self.sleep_interval     : int  = 600

        self._manage_power()

        self.mqtt_manager.set_on_callback(self._on_mqtt_message)

    def _manage_power(self) -> None:
        self.bluetooth_manager.ensure_bluetooth_disabled()

        if ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from machine import Pin
            # pylint: disable=import-error,import-outside-toplevel
            from webrepl import stop

            for pin in UNUSED_PINS:
                Pin(pin, Pin.IN, pull=None)

            stop()

    def _on_mqtt_message(self, topic: str, payload: dict) -> None:
        log_debug(f'Received MQTT message on topic {topic}:\n{dumps(payload)}')

        if topic == f'{TOPIC_ACTION}/{self.device_id}':
            self._handle_action(payload)
        elif topic == f'{TOPIC_DEVICE}/{self.device_id}':
            self._handle_parameters_update(payload)
        elif topic == f'{TOPIC_OTP}/{self.device_id}':
            self._handle_otp(payload)

    # pylint: disable=unused-argument
    def _handle_parameters_update(self, parameters: dict) -> None:
        self.parameters_updated = True

    def _handle_action(self, payload: dict) -> None:
        pass

    def _handle_otp(self, payload: dict) -> None:
        pass

    def register(self) -> None:
        log_debug(f'Registering device {self.device_id}...')

        self.mqtt_manager.publish(f'{TOPIC_REGISTRATION}/{self.device_id}', dumps({
            'device_id'    : self.device_id,
            'app_name'     : NODE_NAME,
            'app_version'  : NODE_VERSION,
            'capabilities' : ','.join(CAPABILITIES),
        }))

    def publish_telemetry(self):
        for sensor in self.sensors:
            try:
                telemetry = sensor.read()
                if telemetry is not None:
                    for data_type, value in telemetry.items():
                        payload = {
                            'device_id' : self.device_id,
                            'data_type' : data_type,
                            'value'     : round(value * 100),
                        }

                        log_debug(f'Publishing telemetry data for device {self.device_id}: {dumps(payload)}')

                        self.mqtt_manager.publish(f'{TOPIC_DEVICE}/{self.device_id}', dumps(payload))
            # pylint: disable=broad-exception-caught
            except Exception as e:
                log_debug(f'Error reading from sensor {sensor.__class__.__name__}: {e}')

    def start(self) -> None:
        self.register()

        self.watchdog.feed()

        deadline = time() + PARAMETERS_UPDATE_TIMEOUT
        while time() < deadline:
            if self.parameters_updated:
                break

            self.watchdog.feed()

            sleep(1)

        if not self.parameters_updated:
            log_debug('Parameters update timeout reached, entering deepsleep mode...')

            self.sleeper.deep_sleep(self.sleep_interval * 1000)
        else:
            self.publish_telemetry()

        self.watchdog.feed()

        self.wifi_manager.ensure_wifi_off()

        log_debug(f'Deep sleeping for {self.sleep_interval} seconds...')
        self.sleeper.deep_sleep(self.sleep_interval * 1000)
