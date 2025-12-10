from esparkcore.routers.base_router import BaseRouter
from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models import Settings
from ..data.repositories import SettingsRepository


class SettingsRouter(BaseRouter):
    def __init__(self, repo: SettingsRepository = None) -> None:
        self.repo: SettingsRepository = repo or SettingsRepository()

        super().__init__(Settings, self.repo, '/api/v1/settings', ['settings'])

    def _setup_routes(self) -> None:
        @self.router.get('/{id}', response_model=Settings)
        async def get_by_id(id: int = Path(..., gt=0), session: AsyncSession = Depends(BaseRouter._get_session)) -> Settings:
            # pylint: disable=unexpected-keyword-arg
            settings = await self.repo.get(session, Settings.id == id)
            if not settings:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            return settings

        super()._setup_routes()
