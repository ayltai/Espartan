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

from src.configs import BUZZER_PIN, CAPABILITY_DOOR_OPEN, CAPABILITY_MOTION, DETECTION_DELAY, MAX_DETECTION_DURATION, MOTION_SENSOR_NAME, SWITCH_NAME


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

        self.sleep_interval = DETECTION_DELAY

        self.detection_enabled      : bool = True
        self.max_detection_duration : int  = MAX_DETECTION_DURATION
        self.last_detection_time    : int  = 0
        self.buzzer_enabled         : bool = True
        self.buzzer_started         : bool = False
        self.warnings_issued        : bool = False

        for trigger in self.triggers:
            trigger.register_callback(self._on_triggered)

    def _handle_parameters_update(self, parameters: dict) -> None:
        self.sleep_interval         = parameters.get('sleep_interval', self.sleep_interval)
        self.max_detection_duration = parameters.get('max_detection_duration', self.max_detection_duration)
        self.detection_enabled      = parameters.get('detection_enabled', self.detection_enabled)
        self.buzzer_enabled         = parameters.get('buzzer_enabled', self.buzzer_enabled)

        super()._handle_parameters_update(parameters)

    # pylint: disable=unused-argument
    def _on_triggered(self, value: bool, trigger: BaseTrigger) -> None:
        log_debug(f'Trigger {trigger.get_name()} detected {str(value)}', self.device_id, self.mqtt_manager)

        if trigger.get_name() == SWITCH_NAME:
            door_open : bool = not value

            self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
                'device_id' : self.device_id,
                'data_type' : CAPABILITY_DOOR_OPEN,
                'value'     : 100 if door_open else 0,
            }))

            if not door_open:
                self._on_door_closed()
        elif trigger.get_name() == MOTION_SENSOR_NAME:
            self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
                'device_id' : self.device_id,
                'data_type' : CAPABILITY_MOTION,
                'value'     : 100 if value else 0,
            }))

            if value:
                self.last_detection_time = time()

    def _on_door_closed(self) -> None:
        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from esparknode.triggers.gpio_interrupt import GpioInterrupt

            for trigger in self.triggers:
                if trigger.get_name() == SWITCH_NAME and isinstance(trigger, GpioInterrupt):
                    gpio_interrupt : GpioInterrupt = trigger
                    door_open      : bool          = True if gpio_interrupt.value() == 0 else False

                    log_debug(f'Door open state: {door_open}', self.device_id, self.mqtt_manager)

                    if not door_open:
                        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
                            'device_id' : self.device_id,
                            'data_type' : CAPABILITY_DOOR_OPEN,
                            'value'     : 0,
                        }))

                        gpio_interrupt.wake_on(0)

                        self.stop_buzzer()

                        for t in self.triggers:
                            t.stop()

                        self.sleeper.deep_sleep(self.sleep_interval * 5 * 1000)

    def _on_door_opened(self) -> None:
        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from esparknode.triggers.gpio_interrupt import GpioInterrupt

            for trigger in self.triggers:
                if trigger.get_name() == SWITCH_NAME and isinstance(trigger, GpioInterrupt):
                    gpio_interrupt : GpioInterrupt = trigger
                    door_open      : bool          = True if gpio_interrupt.value() == 0 else False

                    log_debug(f'Door open state: {door_open}', self.device_id, self.mqtt_manager)

                    if door_open:
                        gpio_interrupt.wake_on(1)

                        self.sleeper.deep_sleep(self.sleep_interval * 5 * 1000)

    def publish_telemetry(self):
        self._on_door_closed()

        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
            'device_id' : self.device_id,
            'data_type' : CAPABILITY_DOOR_OPEN,
            'value'     : 100,
        }))

        self.start_detection()

    def start_detection(self) -> None:
        self.turn_on_light()

        if len(self.triggers) > 0:
            for trigger in self.triggers:
                trigger.start()

            detection_start        = max(self.last_detection_time, time())
            max_detection_duration = self.max_detection_duration

            while self.detection_enabled and (time() - detection_start) < max_detection_duration:
                detection_start = max(self.last_detection_time, detection_start)

                if not self.buzzer_enabled:
                    self.stop_buzzer()

                if time() - detection_start > self.sleep_interval:
                    self._on_door_closed()

                    if not self.warnings_issued:
                        self.warnings_issued = True

                        log_debug('Issuing door-open warnings')

                        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
                            'device_id' : self.device_id,
                            'data_type' : CAPABILITY_DOOR_OPEN,
                            'value'     : 200,
                        }))

                    self.start_buzzer()
                else:
                    self.warnings_issued = False

                    self.stop_buzzer()

                self.watchdog.feed()

                sleep(5)

            self.stop_detection()

        log_debug('Issuing door-open final alert')

        self.mqtt_manager.publish(f'{TOPIC_TELEMETRY}/{self.device_id}', dumps({
            'device_id' : self.device_id,
            'data_type' : CAPABILITY_DOOR_OPEN,
            'value'     : 300,
        }))

        self._on_door_opened()

    def stop_detection(self) -> None:
        self.turn_off_light()
        self.stop_buzzer()

        for trigger in self.triggers:
            trigger.stop()

    def start_buzzer(self) -> None:
        if self.buzzer_enabled and not self.buzzer_started:
            log_debug('Starting buzzer...')

            self.buzzer_started = True

            self._set_pin(BUZZER_PIN, 1)

    def stop_buzzer(self) -> None:
        if self.buzzer_started:
            log_debug('Stopping buzzer...')

            self.buzzer_started = False

            self._set_pin(BUZZER_PIN, 0)

    def turn_on_light(self) -> None:
        self._set_pin(esparknode.configs.LED_PIN, 0)

    def turn_off_light(self) -> None:
        self._set_pin(esparknode.configs.LED_PIN, 1)

    @staticmethod
    def _set_pin(pin: int, value: int) -> None:
        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from machine import Pin

            Pin(pin, Pin.OUT).value(value)
