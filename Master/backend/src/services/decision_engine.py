from typing import Iterable, Optional

from ..data.models import Settings
from ..data.repositories import SettingsRepository
from ..data import async_session
from ..strategies import AvgStrategy, MinStrategy

STRATEGIES = {
    'avg': AvgStrategy,
    'min': MinStrategy,
}


class DecisionEngine:
    def __init__(self):
        self.repo     = SettingsRepository()
        self.strategy = MinStrategy()

    async def decide(self, values: Iterable[float]) -> Optional[bool]:
        async with async_session() as session:
            settings: Settings = await self.repo.get(session, Settings.id == 1)
            if settings:
                self.strategy = STRATEGIES.get(settings.decision_strategy, MinStrategy)()

        return await self.strategy.evaluate(values)
