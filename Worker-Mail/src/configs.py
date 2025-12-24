import esparknode.configs
import esparknode.constants

esparknode.constants.NODE_NAME    = 'Espartan-Mail'
esparknode.constants.NODE_VERSION = '0.5.0'

esparknode.configs.ENVIRONMENT = 'esp32'

CAPABILITY_MAIL : str = 'mail'

esparknode.configs.CAPABILITIES = [
    CAPABILITY_MAIL,
]

esparknode.configs.UNUSED_PINS = [
    0,
    1,
    2,
    5,
    6,
    7,
    9,
    10,
    20,
    21,
]

DOOR_IN_PIN  : int = 3
DOOR_OUT_PIN : int = 4

DOOR_IN_NAME  : str = 'door_in'
DOOR_OUT_NAME : str = 'door_out'
