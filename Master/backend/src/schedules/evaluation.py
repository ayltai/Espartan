from datetime import datetime, timezone

from esparkcore.data.models import Device, OutboxEvent
from esparkcore.data.repositories import DeviceRepository, OutboxRepository, TelemetryRepository
from esparkcore.data import async_session
from esparkcore.utils import log_debug
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models import Relay
from ..data.repositories import RelayRepository
from ..services import DecisionEngine

engine = DecisionEngine()


async def evaluate():
    async with async_session() as session:
        device_repo    = DeviceRepository()
        outbox_repo    = OutboxRepository()
        relay_repo     = RelayRepository()
        telemetry_repo = TelemetryRepository()

        log_debug('Starting evaluation cycle')

        actuators = await device_repo.list_by_capability(session, 'action_relay')
        if not actuators or len(actuators) == 0:
            return

        current_state = await relay_repo.get_current_state(session, actuators[0].id)

        log_debug(f'Current actuator state: {current_state}')

        values: list[float] = []

        # pylint: disable=no-member
        devices = await device_repo.list(session, Device.capabilities.contains('temperature'))
        for device in devices:
            telemetry = await telemetry_repo.get_latest_for_device(session, device.id, 'temperature')
            if telemetry:
                values.append(telemetry.value / 100.0)

        decision = await engine.decide(values)
        if decision is None:
            return

        log_debug(f'Decision made: {"ON" if decision else "OFF"}')

        relay = await _upsert_relay(session, relay_repo, actuators[0].id, 1 if decision else 0)

        await _upsert_event(session, outbox_repo, actuators[0].id, relay.state)

        await session.commit()


async def _upsert_relay(session: AsyncSession, relay_repo: RelayRepository, actuator_id: str, state: int) -> Relay:
    relay = await relay_repo.get_latest(session, actuator_id)
    if relay:
        await relay_repo.update(session, relay, timestamp=datetime.now(timezone.utc), state=state)
    else:
        relay = Relay()
        relay.device_id = actuator_id
        relay.timestamp = datetime.now(timezone.utc)
        relay.state     = state

        await relay_repo.add(session, relay)

    return relay


async def _upsert_event(session: AsyncSession, outbox_repo: OutboxRepository, actuator_id: str, state: int) -> OutboxEvent:
    await outbox_repo.delete_pending(session, actuator_id, 'relay_state_changed')

    event = OutboxEvent()
    event.device_id  = actuator_id
    event.event_type = 'relay_state_changed'
    event.payload    = {
        'device_id' : actuator_id,
        'state'     : state,
    }

    return await outbox_repo.add(session, event)
