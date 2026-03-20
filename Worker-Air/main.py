import esparknode.configs

from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.utils.base_ota_manager import BaseOtaManager
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_crash, log_debug

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
sensors           : list[BaseSensor]

i2c = None

if esparknode.configs.ENVIRONMENT == 'unix':
    from esparknode.networks.dummy_bluetooth import BluetoothManager
    from esparknode.networks.dummy_wifi import WiFiManager
    from esparknode.networks.simple_mqtt import MQTTManager
    from esparknode.sensors.dummy_sensor import DummySensor
    from esparknode.utils.dummy_ota_manager import OtaManager
    from esparknode.utils.dummy_watchdog import Watchdog
    from esparknode.utils.simple_sleeper import Sleeper

    device_id : bytes = b'Worker-Air'

    sensors : list[BaseSensor] = [
        DummySensor(),
    ]

    ota_manager       = OtaManager()
    bluetooth_manager = BluetoothManager()
    watchdog          = Watchdog()
    wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
    mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=''.join(f'{b:02x}' for b in device_id), host=MQTT_HOST)
    sleeper           = Sleeper()
elif esparknode.configs.ENVIRONMENT == 'esp32':
    # pylint: disable=import-error,import-outside-toplevel
    from machine import unique_id

    from esparknode.networks.esp32_bluetooth import BluetoothManager
    from esparknode.networks.esp32_mqtt import MQTTManager
    from esparknode.networks.esp32_wifi import WiFiManager
    from esparknode.sensors.scd4x_sensor import SCD4X
    from esparknode.sensors.sps30_sensor import SPS30
    from esparknode.utils.esp32_ota_manager import OtaManager
    from esparknode.utils.safe_i2c import SafeI2C
    from esparknode.utils.esp32_sleeper import Sleeper
    from esparknode.utils.esp32_watchdog import Watchdog

    device_id = unique_id()

    i2c = SafeI2C(0, scl=src.configs.SCL_PIN, sda=src.configs.SDA_PIN, freq=100_000, timeout=100_000)

    sensors = [
        SCD4X(i2c=i2c, address=src.configs.SCD40_I2C_ADDRESS),
        SPS30(i2c=i2c, address=src.configs.SPS30_I2C_ADDRESS),
    ]

    ota_manager       = OtaManager(OTA_URL)
    bluetooth_manager = BluetoothManager()
    watchdog          = Watchdog()
    wifi_manager      = WiFiManager(watchdog=watchdog, ssid=WIFI_SSID, password=WIFI_PASSWORD)
    mqtt_manager      = MQTTManager(wifi_manager=wifi_manager, watchdog=watchdog, device_id=''.join(f'{b:02x}' for b in device_id), host=MQTT_HOST)
    sleeper           = Sleeper()
else:
    raise RuntimeError(f'Unknown environment in configuration: {esparknode.configs.ENVIRONMENT}')

log_debug(f'Starting device with ID: {id}')

try:
    WorkerNode(
        device_id         = ''.join(f'{b:02x}' for b in device_id),
        sleeper           = sleeper,
        watchdog          = watchdog,
        wifi_manager      = wifi_manager,
        mqtt_manager      = mqtt_manager,
        bluetooth_manager = bluetooth_manager,
        ota_manager       = ota_manager,
        sensors           = sensors,
        i2c               = i2c,
    ).start()
except Exception as e:
    log_crash(e, device_id=''.join(f'{b:02x}' for b in device_id), mqtt_manager=mqtt_manager)
