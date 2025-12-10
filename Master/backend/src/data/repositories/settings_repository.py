from esparkcore.data.repositories import AsyncRepository

from ..models import Settings


class SettingsRepository(AsyncRepository[Settings]):
    def __init__(self):
        super().__init__(Settings)
