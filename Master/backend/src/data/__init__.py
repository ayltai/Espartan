from esparkcore.data import async_session
from esparkcore.data.models import AppVersion
from esparkcore.data.repositories import AppVersionRepository
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Settings
from .repositories import SettingsRepository


async def init_settings() -> None:
    async with async_session() as session:
        await ensure_settings(session)
        await ensure_app(session, 'Espartan-Door', '0.5.0')
        await ensure_app(session, 'Espartan-Mail', '0.5.0')
        await ensure_app(session, 'Espartan-Thermo', '0.5.0')

        await session.commit()


async def ensure_settings(session: AsyncSession) -> None:
    settings = Settings()
    repo     = SettingsRepository()

    existing = await repo.get(session, Settings.id == 1)
    if not existing:
        settings.id                = 1
        settings.threshold_on      = 17.5
        settings.threshold_off     = 18.0
        settings.decision_strategy = 'avg'

        session.add(settings)


async def ensure_app(session: AsyncSession, app_name: str, app_version: str) -> None:
    version = AppVersion()
    repo    = AppVersionRepository()

    existing = await repo.get(session, AppVersion.id == app_name)
    if not existing:
        version.id      = app_name
        version.version = app_version

        session.add(version)
