from pytest import mark

from src.data.models import Settings
from src.data.repositories import SettingsRepository


@mark.asyncio
async def test_settings_repository_init():
    repo = SettingsRepository()

    assert repo.model is Settings
