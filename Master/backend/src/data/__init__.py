from esparkcore.data import async_session

from .models import Settings
from .repositories import SettingsRepository


async def init_settings():
    async with async_session() as session:
        settings = Settings()
        repo     = SettingsRepository()

        existing = await repo.get(session, Settings.id == 1)
        if not existing:
            settings.id                = 1
            settings.threshold_on      = 17.5
            settings.threshold_off     = 18.5
            settings.decision_strategy = 'min'

            session.add(settings)

            await session.commit()
