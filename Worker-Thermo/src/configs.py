import esparknode.configs

esparknode.configs.ENVIRONMENT = 'unix'

esparknode.configs.CAPABILITIES = [
    'action_relay',
    'battery',
    'humidity',
    'temperature',
]

esparknode.configs.UNUSED_PINS = [
    0,
    3,
    4,
    5,
    6,
    7,
    9,
    10,
]

SCL_PIN : int = 20
SDA_PIN : int = 21

VOLTAGE_PIN : int = 1
RELAY_PIN   : int = 2

VOLTAGE_FULL  : float = 3 * 1.5
VOLTAGE_EMPTY : float = 3 * 1.1

VOLTAGE_DIVIDER_RATIO : float = 5.0
