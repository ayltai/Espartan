from json import dumps
from time import sleep

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

from src.configs import CAPABILITY_MAIL


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

        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from esparknode.utils.esp32_gpio import GpioPin

            GpioPin(8).set_low()

    # pylint: disable=unused-argument
    def _on_triggered(self, value: bool, trigger: BaseTrigger, pin_index: int = 0) -> None:
        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
            'device_id' : self.device_id,
            'data_type' : CAPABILITY_MAIL,
            'value'     : (100 if value else -100) if pin_index == 0 else (200 if value else -200) if pin_index == 1 else 0,
        }))

    def publish_telemetry(self) -> None:
        if len(self.triggers) > 0:
            for trigger in self.triggers:
                if esparknode.configs.ENVIRONMENT == 'esp32':
                    # pylint: disable=import-error,import-outside-toplevel
                    from machine import PIN_WAKE, wake_reason

                    from esparknode.triggers.gpio_interrupt import GpioInterrupt

                    if isinstance(trigger, GpioInterrupt):
                        gpio_interrupt     : GpioInterrupt = trigger
                        mail_in_door_open  : bool          = gpio_interrupt.value(0) == 1
                        mail_out_door_open : bool          = gpio_interrupt.value(1) == 1

                        self._on_triggered(True if wake_reason() == PIN_WAKE else mail_in_door_open, trigger, 0)
                        self._on_triggered(mail_out_door_open, trigger, 1)

        self.start_detection()

    def start_detection(self) -> None:
        if len(self.triggers) > 0:
            if esparknode.configs.ENVIRONMENT == 'esp32':
                # pylint: disable=import-error,import-outside-toplevel
                from esparknode.triggers.gpio_interrupt import GpioInterrupt

                while True:
                    for trigger in self.triggers:
                        if isinstance(trigger, GpioInterrupt):
                            gpio_interrupt     : GpioInterrupt = trigger
                            mail_in_door_open  : bool          = gpio_interrupt.value(0) == 1
                            mail_out_door_open : bool          = gpio_interrupt.value(1) == 1

                            gpio_interrupt.start(0)
                            gpio_interrupt.start(1)

                            if mail_in_door_open or mail_out_door_open:
                                self.watchdog.feed()

                                sleep(5)
                            else:
                                gpio_interrupt.wake_on(1)

                                self.sleeper.deep_sleep(24 * 60 * 60 * 1000)
