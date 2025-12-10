from datetime import datetime
from typing import Optional, Sequence

from esparkcore.data.repositories.base_repository import AsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_

from ..models import Relay


class RelayRepository(AsyncRepository[Relay]):
    def __init__(self):
        super().__init__(Relay)

    async def get_current_state(self, session: AsyncSession, device_id: str) -> Optional[int]:
        # pylint: disable=no-member,unexpected-keyword-arg
        results = await self.list(session, Relay.device_id == device_id, order_by=Relay.timestamp.desc(), limit=1)
        return results[0].state if results else None

    async def get_latest(self, session: AsyncSession, device_id: str) -> Optional[Relay]:
        # pylint: disable=no-member,unexpected-keyword-arg
        results = await self.list(session, Relay.device_id == device_id, order_by=Relay.timestamp.desc(), limit=1)
        return results[0] if results else None

    async def list_recent(self, session: AsyncSession, device_id: str, since: datetime) -> Sequence[Relay]:
        # pylint: disable=no-member
        return await self.list(session, and_(Relay.device_id == device_id, Relay.timestamp >= since), order_by=Relay.timestamp.desc())
