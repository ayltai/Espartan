from json import dumps
from os import getenv

from aiomqtt import Client

from esparkcore.constants import ENV_MQTT_HOST, ENV_MQTT_PORT, TOPIC_ACTION
from esparkcore.data.repositories import DeviceRepository
from esparkcore.data import async_session
from esparkcore.utils import log_debug


async def housekeep():
    async with async_session() as session:
        device_repo = DeviceRepository()

        log_debug('Starting housekeeping cycle')

        actuators = await device_repo.list_by_capability(session, 'action_calibrate')
        if not actuators or len(actuators) == 0:
            return

        for actuator in actuators:
            async with Client(getenv(ENV_MQTT_HOST, 'localhost'), int(getenv(ENV_MQTT_PORT, '1883'))) as client:
                await client.publish(f'{TOPIC_ACTION}/{actuator.id}', dumps({
                    'state': 1,
                }), qos=1)
