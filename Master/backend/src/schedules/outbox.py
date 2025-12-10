from esparkcore.data.repositories import DeviceRepository
from esparkcore.data import async_session
from esparkcore.schedules import consume_outbox


async def process_outbox():
    async with async_session() as session:
        device_repo = DeviceRepository()
        actuators   = await device_repo.list_by_capability(session, 'action_relay')

        if not actuators or len(actuators) == 0:
            return

        await consume_outbox(actuators[0].id, 'relay_state_changed')
