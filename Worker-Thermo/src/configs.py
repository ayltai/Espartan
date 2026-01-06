import esparknode.configs
import esparknode.constants

esparknode.constants.NODE_NAME    = 'Espartan-Thermo'
esparknode.constants.NODE_VERSION = '0.5.1'

esparknode.configs.ENVIRONMENT = 'unix'

MODE = 'actuator'
# MODE = 'sensor'

if MODE == 'actuator':
    esparknode.configs.CAPABILITIES = [
        'action_relay',
        'humidity',
        'temperature',
    ]
elif MODE == 'sensor':
    esparknode.configs.CAPABILITIES = [
        'battery',
        'humidity',
        'temperature',
    ]

if MODE == 'actuator':
    esparknode.configs.UNUSED_PINS = [
        0,
        1,
        6,
        7,
        9,
        10,
        20,
        21,
    ]
elif MODE == 'sensor':
    esparknode.configs.UNUSED_PINS = [
        0,
        2,
        3,
        6,
        7,
        9,
        10,
        20,
        21,
    ]

SDA_PIN : int = 4
SCL_PIN : int = 5

VOLTAGE_PIN     : int = 1
RELAY_SET_PIN   : int = 2
RELAY_RESET_PIN : int = 3

VOLTAGE_FULL  : float = 3 * 1.375
VOLTAGE_EMPTY : float = 3 * 1.15

VOLTAGE_DIVIDER_RATIO : float = 5.0
