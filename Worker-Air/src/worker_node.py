from random import choice
from time import sleep, time

import esparknode.configs

from esparknode.base_node import BaseNode
from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.base_ota_manager import BaseOtaManager
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug

from src.configs import CAPABILITY_CO2, CAPABILITY_PM1_0, CAPABILITY_PM2_5, CAPABILITY_PM4_0, CAPABILITY_PM10, SSD1306_DISPLAY_HEIGHT, SSD1306_DISPLAY_WIDTH, SSD1306_I2C_ADDRESS, THRESHOLDS

STABILIZATION_DELAY : int = 15
HOUSEKEEP_DELAY     : int = 15


class WorkerNode(BaseNode):
    def __init__(
            self,
            device_id         : str,
            sleeper           : BaseSleeper,
            watchdog          : BaseWatchdog,
            wifi_manager      : BaseWiFiManager,
            mqtt_manager      : BaseMQTTManager,
            bluetooth_manager : BaseBluetoothManager = None,
            ota_manager       : BaseOtaManager       = None,
            sensors           : list[BaseSensor]     = None,
            triggers          : list[BaseTrigger]    = None,
            i2c=None,
    ):
        super().__init__(
            device_id=device_id,
            sleeper=sleeper,
            watchdog=watchdog,
            wifi_manager=wifi_manager,
            mqtt_manager=mqtt_manager,
            bluetooth_manager=bluetooth_manager,
            ota_manager=ota_manager,
            sensors=sensors,
            triggers=triggers,
        )

        self.altitude: int = 0

        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-outside-toplevel
            from src.ssd1306 import SSD1306_I2C

            self.display = SSD1306_I2C(SSD1306_DISPLAY_WIDTH, SSD1306_DISPLAY_HEIGHT, i2c=i2c, addr=SSD1306_I2C_ADDRESS)
            self.display.contrast(10)
            self.display.invert(choice((True, False)))
            self.display.fill(0)
            self.display.text('Initialising...', 8, 28)
            self.display.show()

    def _handle_parameters_update(self, parameters: dict) -> None:
        self.sleep_interval     = parameters.get('sleep_interval', self.sleep_interval)
        self.deep_sleep_enabled = parameters.get('deep_sleep_enabled', self.deep_sleep_enabled)
        self.altitude           = parameters.get('altitude', self.altitude)

        super()._handle_parameters_update(parameters)

    def _handle_action(self, payload: dict) -> None:
        state : bool = payload['state'] == 1

        log_debug(f'Setting state to: {state}')

        for sensor in self.sensors:
            if state and sensor.__class__.__name__ in ['SPS30', 'SCD4X']:
                sensor.housekeep()

                deadline = time() + HOUSEKEEP_DELAY
                while time() < deadline:
                    self.watchdog.feed()

                    sleep(1)

    def publish_telemetry(self) -> dict:
        for sensor in self.sensors:
            if sensor.__class__.__name__ in ['SPS30', 'SCD4X']:
                if sensor.__class__.__name__ == 'SCD4X':
                    sensor.configure_altitude(self.altitude)

                sensor.stop()
                sensor.start()

        deadline = time() + STABILIZATION_DELAY
        while time() < deadline:
            self.watchdog.feed()

            sleep(1)

        measurements = super().publish_telemetry()

        self._update_display(measurements)
        self._trigger_alert(measurements)

        return measurements

    def _update_display(self, measurements: dict) -> None:
        if self.display is not None:
            self.display.fill(0)

            self.display.text(f'PM1   : {measurements.get(CAPABILITY_PM1_0, 0):.1f}' if CAPABILITY_PM1_0 in measurements.keys() else 'PM1   : -', 8, 4)
            self.display.text(f'PM2.5 : {measurements.get(CAPABILITY_PM2_5, 0):.1f}' if CAPABILITY_PM2_5 in measurements.keys() else 'PM2.5 : -', 8, 16)
            self.display.text(f'PM4   : {measurements.get(CAPABILITY_PM4_0, 0):.1f}' if CAPABILITY_PM4_0 in measurements.keys() else 'PM4   : -', 8, 28)
            self.display.text(f'PM10  : {measurements.get(CAPABILITY_PM10, 0):.1f}' if CAPABILITY_PM10 in measurements.keys() else 'PM10  : -', 8, 40)
            self.display.text(f'CO2   : {round(measurements.get(CAPABILITY_CO2, 0))}' if CAPABILITY_CO2 in measurements.keys() else 'CO2   : -', 8, 52)

            self.display.show()

    @staticmethod
    def _trigger_alert(measurements: dict) -> None:
        ratios = [
            measurements.get(CAPABILITY_PM1_0, 0) / THRESHOLDS[CAPABILITY_PM1_0],
            measurements.get(CAPABILITY_PM2_5, 0) / THRESHOLDS[CAPABILITY_PM2_5],
            measurements.get(CAPABILITY_PM4_0, 0) / THRESHOLDS[CAPABILITY_PM4_0],
            measurements.get(CAPABILITY_PM10, 0) / THRESHOLDS[CAPABILITY_PM10],
            measurements.get(CAPABILITY_CO2, 0) / THRESHOLDS[CAPABILITY_CO2],
        ]

        if esparknode.configs.ENVIRONMENT == 'esp32':
            # pylint: disable=import-error,import-outside-toplevel
            from esparknode.utils.esp32_gpio import GpioPin

            if any(ratio > 1 for ratio in ratios):
                GpioPin(8).set_low()
            else:
                GpioPin(8).set_high()
