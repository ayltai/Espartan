import esparknode.configs

from esparknode.actions.base_relay import BaseRelay
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.logging import log_crash, log_debug

import src.configs

from src.secrets import MQTT_HOST, WIFI_PASSWORD, WIFI_SSID
from src.worker_node import WorkerNode

if esparknode.configs.ENVIRONMENT == 'unix':
    from esparknode.actions.simple_relay import Relay
    from esparknode.networks.dummy_bluetooth import BluetoothManager
    from esparknode.networks.dummy_wifi import WiFiManager
    from esparknode.networks.simple_mqtt import MQTTManager
    from esparknode.sensors.dummy_sensor import DummySensor
    from esparknode.utils.simple_sleeper import Sleeper
    from esparknode.utils.dummy_watchdog import Watchdog

    device_id : bytes = b'Worker-Thermo'

    actions : list[BaseRelay] = [
        Relay(),
    ]

    sensors : list[BaseSensor] = [
        DummySensor(),
    ]
elif esparknode.configs.ENVIRONMENT == 'esp32':
    from machine import unique_id

    from esparknode.actions.esp32_relay import Relay
    from esparknode.networks.esp32_bluetooth import BluetoothManager
    from esparknode.networks.esp32_mqtt import MQTTManager
    from esparknode.networks.esp32_wifi import WiFiManager
    from esparknode.sensors.sht20_sensor import SHT20Sensor
    from esparknode.sensors.voltage_sensor import VoltageSensor
    from esparknode.utils.esp32_sleeper import Sleeper
    from esparknode.utils.esp32_watchdog import Watchdog

    device_id : bytes = unique_id()

    actions : list[BaseRelay] = [
        Relay(src.configs.RELAY_PIN),
    ]

    sensors : list[BaseSensor] = [
        SHT20Sensor(scl_pin=src.configs.SCL_PIN, sda_pin=src.configs.SDA_PIN),
        VoltageSensor(pin=src.configs.VOLTAGE_PIN, voltage_full=src.configs.VOLTAGE_FULL, voltage_empty=src.configs.VOLTAGE_EMPTY, voltage_divider_ratio=src.configs.VOLTAGE_DIVIDER_RATIO),
    ]
else:
    raise RuntimeError(f'Unknown environment in configuration: {esparknode.configs.ENVIRONMENT}')

id                = ''.join(f'{b:02x}' for b in device_id)
sleeper           = Sleeper()
watchdog          = Watchdog()
bluetooth_manager = BluetoothManager()
wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=id, host=MQTT_HOST)

log_debug(f'Starting device with ID: {id}')

try:
    WorkerNode(
        device_id         = id,
        sleeper           = sleeper,
        watchdog          = watchdog,
        wifi_manager      = wifi_manager,
        mqtt_manager      = mqtt_manager,
        bluetooth_manager = bluetooth_manager,
        actions           = actions,
        sensors           = sensors,
    ).start()
except Exception as e:
    log_crash(e, device_id=id, mqtt_manager=mqtt_manager)
