import esparknode.configs
import esparknode.constants

esparknode.constants.NODE_NAME    = 'Espartan-Air'
esparknode.constants.NODE_VERSION = '0.6.1'

esparknode.configs.ENVIRONMENT = 'unix'

esparknode.configs.WATCHDOG_ENABLED = False

CAPABILITY_PM1_0 = 'pm1.0'
CAPABILITY_PM2_5 = 'pm2.5'
CAPABILITY_PM4_0 = 'pm4.0'
CAPABILITY_PM10  = 'pm10'
CAPABILITY_CO2   = 'co2'

esparknode.configs.CAPABILITIES = [
    'action_calibrate',
    CAPABILITY_PM1_0,
    CAPABILITY_PM2_5,
    CAPABILITY_PM4_0,
    CAPABILITY_PM10,
    CAPABILITY_CO2,
]

esparknode.configs.UNUSED_PINS = [
    0,
    1,
    2,
    3,
    4,
    5,
    9,
    10,
    20,
    21,
]

SDA_PIN = 6
SCL_PIN = 7

SPS30_I2C_ADDRESS = 0x69
SCD40_I2C_ADDRESS = 0x62

SSD1306_I2C_ADDRESS    = 0x3C
SSD1306_DISPLAY_WIDTH  = 128
SSD1306_DISPLAY_HEIGHT = 64

THRESHOLDS = {
    CAPABILITY_PM1_0 : 10.0,
    CAPABILITY_PM2_5 : 12.0,
    CAPABILITY_PM4_0 : 25.0,
    CAPABILITY_PM10  : 50.0,
    CAPABILITY_CO2   : 1000.0,
}
