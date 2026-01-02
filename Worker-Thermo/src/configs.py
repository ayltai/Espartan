import esparknode.configs
import esparknode.constants

esparknode.constants.NODE_NAME    = 'Espartan-Thermo'
esparknode.constants.NODE_VERSION = '0.5.1'

esparknode.configs.ENVIRONMENT = 'esp32'

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
        3,
        4,
        5,
        6,
        7,
        9,
        10,
    ]
elif MODE == 'sensor':
    esparknode.configs.UNUSED_PINS = [
        0,
        2,
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

VOLTAGE_PIN     : int = 1
RELAY_SET_PIN   : int = 2
RELAY_RESET_PIN : int = 3

VOLTAGE_FULL  : float = 3 * 1.3
VOLTAGE_EMPTY : float = 3 * 1.1

VOLTAGE_DIVIDER_RATIO : float = 5.0
