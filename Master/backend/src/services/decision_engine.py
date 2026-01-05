from typing import Iterable, Optional

from ..data.models import Settings
from ..data.repositories import SettingsRepository
from ..data import async_session
from ..strategies import AvgStrategy, MinStrategy
from ..utils import AppConfig

STRATEGIES = {
    'avg': AvgStrategy,
    'min': MinStrategy,
}

app_config = AppConfig()


class DecisionEngine:
    def __init__(self):
        self.repo     = SettingsRepository()
        self.strategy = MinStrategy()

    async def decide(self, values: Iterable[float]) -> Optional[bool]:
        async with async_session() as session:
            settings: Settings = await self.repo.get(session, Settings.id == 1)
            if settings:
                self.strategy = STRATEGIES.get(settings.decision_strategy, MinStrategy)()

        for value in values:
            if value < app_config.heating_min_temperature:
                return True

        return await self.strategy.evaluate(values)
