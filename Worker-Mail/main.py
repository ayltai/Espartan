import esparknode.configs


from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.base_ota_manager import BaseOtaManager
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_crash

import src.configs

from src.secrets import MQTT_HOST, OTA_URL, WIFI_PASSWORD, WIFI_SSID
from src.worker_node import WorkerNode

device_id         : bytes
watchdog          : BaseWatchdog
bluetooth_manager : BaseBluetoothManager
wifi_manager      : BaseWiFiManager
mqtt_manager      : BaseMQTTManager
ota_manager       : BaseOtaManager
sleeper           : BaseSleeper
triggers          : list[BaseTrigger]

if esparknode.configs.ENVIRONMENT == 'unix':
    from esparknode.networks.dummy_bluetooth import BluetoothManager
    from esparknode.networks.dummy_wifi import WiFiManager
    from esparknode.networks.simple_mqtt import MQTTManager
    from esparknode.utils.dummy_ota_manager import OtaManager
    from esparknode.utils.dummy_watchdog import Watchdog
    from esparknode.utils.simple_sleeper import Sleeper

    device_id         = b'Worker-Mail'
    triggers          = []
    ota_manager       = OtaManager()
    bluetooth_manager = BluetoothManager()
    watchdog          = Watchdog()
    wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
    mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=''.join(f'{b:02x}' for b in device_id), host=MQTT_HOST)
    sleeper           = Sleeper()
elif esparknode.configs.ENVIRONMENT == 'esp32':
    from machine import Pin, unique_id

    from esparknode.networks.esp32_bluetooth import BluetoothManager
    from esparknode.networks.esp32_mqtt import MQTTManager
    from esparknode.networks.esp32_wifi import WiFiManager
    from esparknode.triggers.gpio_interrupt import GpioInterrupt
    from esparknode.utils.esp32_ota_manager import OtaManager
    from esparknode.utils.esp32_sleeper import Sleeper
    from esparknode.utils.esp32_watchdog import Watchdog

    device_id = unique_id()

    triggers = [
        GpioInterrupt(pins=[src.configs.DOOR_IN_PIN, src.configs.DOOR_OUT_PIN], pull=Pin.PULL_UP),
    ]

    ota_manager       = OtaManager(OTA_URL)
    bluetooth_manager = BluetoothManager()
    watchdog          = Watchdog()
    wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
    mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=''.join(f'{b:02x}' for b in device_id), host=MQTT_HOST)
    sleeper           = Sleeper()
else:
    raise RuntimeError(f'Unknown environment in configuration: {esparknode.configs.ENVIRONMENT}')

print(f'Starting device with ID: {id}')

try:
    WorkerNode(
        device_id         = ''.join(f'{b:02x}' for b in device_id),
        sleeper           = sleeper,
        watchdog          = watchdog,
        wifi_manager      = wifi_manager,
        mqtt_manager      = mqtt_manager,
        bluetooth_manager = bluetooth_manager,
        ota_manager       = ota_manager,
        triggers          = triggers,
    ).start()
except Exception as e:
    log_crash(e, device_id=''.join(f'{b:02x}' for b in device_id), mqtt_manager=mqtt_manager)
