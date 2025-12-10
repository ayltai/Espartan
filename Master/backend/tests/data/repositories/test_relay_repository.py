from pytest import mark

from unittest.mock import AsyncMock

from src.data.models import Relay
from src.data.repositories import RelayRepository


@mark.asyncio
async def test_get_current_state():
    repo    = RelayRepository()
    session = AsyncMock()
    relay   = Relay(device_id='dev1', state=1)

    repo.list = AsyncMock(return_value=[relay])

    state = await repo.get_current_state(session, 'dev1')

    assert state == 1


@mark.asyncio
async def test_get_latest():
    repo    = RelayRepository()
    session = AsyncMock()
    relay   = Relay(device_id='dev1', state=1)

    repo.list = AsyncMock(return_value=[relay])

    latest = await repo.get_latest(session, 'dev1')

    assert latest == relay
