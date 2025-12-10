from typing import Iterable, Optional

from ..data.models import Settings
from ..data.repositories import SettingsRepository
from ..data import async_session
from .base_strategy import BaseStrategy


class MinStrategy(BaseStrategy):
    def __init__(self):
        self.repo = SettingsRepository()

    async def evaluate(self, values: Iterable[float]) -> Optional[bool]:
        if not values:
            return None

        async with async_session() as session:
            # pylint: disable=unexpected-keyword-arg
            settings = await self.repo.get(session, Settings.id == 1)

            current_min = min(values)
            if current_min < settings.threshold_on:
                return True

            if current_min > settings.threshold_off:
                return False

        return None
