import esparknode.configs

esparknode.configs.ENVIRONMENT = 'unix'

CAPABILITY_DOOR_OPEN : str = 'door_open'
CAPABILITY_MOTION    : str = 'motion'

esparknode.configs.CAPABILITIES = [
    CAPABILITY_DOOR_OPEN,
    CAPABILITY_MOTION,
]

esparknode.configs.UNUSED_PINS = [
    0,
    1,
    2,
    5,
    6,
    7,
    8,
    9,
    10,
    20,
    21,
]

MOTION_SENSOR_PIN : int = 3
SWITCH_PIN        : int = 4
BUZZER_PIN        : int = 10

MOTION_SENSOR_NAME : str = 'motion'
SWITCH_NAME        : str = 'switch'

DETECTION_DELAY        : int = 180
MAX_DETECTION_DURATION : int = 360
