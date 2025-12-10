import esparknode.configs

from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.logging import log_crash

import src.configs

from src.secrets import MQTT_HOST, WIFI_PASSWORD, WIFI_SSID
from src.worker_node import WorkerNode

if esparknode.configs.ENVIRONMENT == 'unix':
    from esparknode.networks.dummy_bluetooth import BluetoothManager
    from esparknode.networks.dummy_wifi import WiFiManager
    from esparknode.networks.simple_mqtt import MQTTManager
    from esparknode.utils.simple_sleeper import Sleeper
    from esparknode.utils.dummy_watchdog import Watchdog

    device_id : bytes             = b'Worker-Door'
    triggers  : list[BaseTrigger] = []
elif esparknode.configs.ENVIRONMENT == 'esp32':
    from machine import Pin, unique_id

    from esparknode.networks.esp32_bluetooth import BluetoothManager
    from esparknode.networks.esp32_mqtt import MQTTManager
    from esparknode.networks.esp32_wifi import WiFiManager
    from esparknode.triggers.gpio_interrupt import GpioInterrupt
    from esparknode.utils.esp32_sleeper import Sleeper
    from esparknode.utils.esp32_watchdog import Watchdog

    device_id : bytes = unique_id()

    triggers : list[BaseTrigger] = [
        GpioInterrupt(pin=src.configs.SWITCH_PIN, pull=Pin.PULL_UP, name=src.configs.SWITCH_NAME),
        GpioInterrupt(pin=src.configs.MOTION_SENSOR_PIN, name=src.configs.MOTION_SENSOR_NAME),
    ]
else:
    raise RuntimeError(f'Unknown environment in configuration: {esparknode.configs.ENVIRONMENT}')

id                = ''.join(f'{b:02x}' for b in device_id)
sleeper           = Sleeper()
watchdog          = Watchdog()
bluetooth_manager = BluetoothManager()
wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=id, host=MQTT_HOST)

print(f'Starting device with ID: {id}')

try:
    WorkerNode(
        device_id         = id,
        sleeper           = sleeper,
        watchdog          = watchdog,
        wifi_manager      = wifi_manager,
        mqtt_manager      = mqtt_manager,
        bluetooth_manager = bluetooth_manager,
        triggers          = triggers,
    ).start()
except Exception as e:
    log_crash(e, device_id=id, mqtt_manager=mqtt_manager)
