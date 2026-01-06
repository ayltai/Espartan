ENVIRONMENT            : str  = 'unix'
LOG_FORWARDING_ENABLED : bool = False

CAPABILITIES : list[str] = [
    'battery',
    'temperature',
    'humidity',
    # 'pressure',
    # 'air_quality',
    # 'light_level',
    # 'action_light',
    'action_relay',
]

WATCHDOG_ENABLED : bool = True
WATCHDOG_TIMEOUT : int  = 15000

MQTT_TIMEOUT   : int = 20
MQTT_KEEPALIVE : int = 60

PARAMETERS_UPDATE_TIMEOUT : int = 20
SENSOR_RETRIES            : int = 5

LED_PIN : int = 8

UART_ID       : int = 1
UART_BAUDRATE : int = 256000
UART_RX_PIN   : int = 20
UART_TX_PIN   : int = 21

UNUSED_PINS : list[int] = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    # 8,
    9,
    10,
    # 20,
    # 21,
]
