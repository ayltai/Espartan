from io import StringIO
from json import dumps

import esparknode.configs

from esparknode.constants import TOPIC_CRASH
from esparknode.networks.base_mqtt import BaseMQTTManager


def log_debug(message: str, device_id: str = None, mqtt_manager: BaseMQTTManager = None) -> None:
    if esparknode.configs.LOG_FORWARDING_ENABLED and device_id and mqtt_manager:
        mqtt_manager.publish(f'{TOPIC_CRASH}/{device_id}', dumps({
            'debug_message' : f'[DEBUG] {message}',
        }))
    else:
        print(f'[DEBUG] {message}')


def log_error(e: Exception, device_id: str = None, mqtt_manager: BaseMQTTManager = None) -> None:
    if esparknode.configs.LOG_FORWARDING_ENABLED and device_id and mqtt_manager:
        mqtt_manager.publish(f'{TOPIC_CRASH}/{device_id}', dumps({
            'error_message' : f'[ERROR] {type(e).__name__}: {e}',
        }))
    else:
        print(f'[ERROR] {type(e).__name__}: {e}')

    raise e


def log_crash(e: Exception, device_id: str, mqtt_manager: BaseMQTTManager) -> None:
    buffer = StringIO()

    if esparknode.configs.ENVIRONMENT == 'esp32':
        # pylint: disable=import-outside-toplevel,no-name-in-module
        from sys import print_exception

        print_exception(e, buffer)

    mqtt_manager.publish(f'{TOPIC_CRASH}/{device_id}', dumps({
        'error_message' : str(e),
        'error_trace'   : buffer.getvalue() if esparknode.configs.ENVIRONMENT == 'esp32' else '',
    }), retain=True)
