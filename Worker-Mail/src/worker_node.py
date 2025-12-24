from json import dumps
from time import sleep, time

import esparknode.configs

from esparknode.constants import TOPIC_TELEMETRY
from esparknode.base_node import BaseNode
from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug

from src.configs import CAPABILITY_MAIL, DOOR_IN_NAME, DOOR_IN_PIN, DOOR_OUT_NAME, DOOR_OUT_PIN


class WorkerNode(BaseNode):
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
        super().__init__(
            device_id=device_id,
            sleeper=sleeper,
            watchdog=watchdog,
            wifi_manager=wifi_manager,
            mqtt_manager=mqtt_manager,
            bluetooth_manager=bluetooth_manager,
            sensors=sensors,
            triggers=triggers,
        )

        self.parameters_updated = True

        for trigger in self.triggers:
            trigger.register_callback(self._on_triggered)

    # pylint: disable=unused-argument
    def _on_triggered(self, value: bool, trigger: BaseTrigger) -> None:
        log_debug(f'Trigger {trigger.get_name()} detected {str(value)}', self.device_id, self.mqtt_manager)

        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
            'device_id' : self.device_id,
            'data_type' : CAPABILITY_MAIL,
            'value'     : (100 if value else -100) if trigger.get_name() == DOOR_IN_NAME else (200 if value else -200) if trigger.get_name() == DOOR_OUT_NAME else 0,
        }))

    def publish_telemetry(self) -> None:
        if len(self.triggers) > 0:
            for trigger in self.triggers:
                if esparknode.configs.ENVIRONMENT == 'esp32':
                    # pylint: disable=import-error,import-outside-toplevel
                    from esparknode.triggers.gpio_interrupt import GpioInterrupt

                    if (trigger.get_name() == DOOR_IN_NAME or trigger.get_name() == DOOR_OUT_NAME) and isinstance(trigger, GpioInterrupt):
                        gpio_interrupt : GpioInterrupt = trigger
                        door_open      : bool          = True if gpio_interrupt.value() == 0 else False

                        log_debug(f'Publishing telemetry for trigger {trigger.get_name()}: {str(door_open)}', self.device_id, self.mqtt_manager)

                        self._on_triggered(door_open, trigger)

        self.start_detection()

    def start_detection(self) -> None:
        if len(self.triggers) > 0:
            for trigger in self.triggers:
                if esparknode.configs.ENVIRONMENT == 'esp32':
                    # pylint: disable=import-error,import-outside-toplevel
                    from esparknode.triggers.gpio_interrupt import GpioInterrupt

                    if (trigger.get_name() == DOOR_IN_NAME or trigger.get_name() == DOOR_OUT_NAME) and isinstance(trigger, GpioInterrupt):
                        gpio_interrupt : GpioInterrupt = trigger

                        gpio_interrupt.wake_on(0)

                        self.sleeper.deep_sleep(0)
