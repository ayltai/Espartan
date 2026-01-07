from asyncio import create_task
from contextlib import asynccontextmanager
from os import getenv, path

from esparkcore.data.repositories import AppVersionRepository, DeviceRepository, NotificationRepository, TelemetryRepository, TriggerRepository
from esparkcore.data import init_db
from esparkcore.routers import AppVersionRouter, DeviceRouter, NotificationRouter, TelemetryRouter, TriggerRouter
from esparkcore.schedules import start_scheduler
from esparkcore.services import MQTTManager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sentry_sdk import init

from .data.repositories import RelayRepository, SettingsRepository
from .data import init_settings
from .routers import RelayRouter, SettingsRouter
from .schedules import evaluate, process_outbox
from .utils import AppConfig

app_config        = AppConfig()
device_repo       = DeviceRepository()
notification_repo = NotificationRepository()
telemetry_repo    = TelemetryRepository()
trigger_repo      = TriggerRepository()
version_repo      = AppVersionRepository()


class SpaStaticFiles(StaticFiles):
    # pylint: disable=redefined-outer-name
    def lookup_path(self, path: str):
        full_path, stat_result = super().lookup_path(path)
        if stat_result is None:
            full_path, stat_result = super().lookup_path('index.html')
        return full_path, stat_result


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    await init_settings()

    scheduler = await start_scheduler()
    scheduler.add_job(evaluate, 'interval', minutes=app_config.heating_evaluation_interval, id='evaluation_job', replace_existing=True)
    scheduler.add_job(process_outbox, 'interval', minutes=app_config.heating_evaluation_interval, id='outbox_consumer_job', replace_existing=True)

    create_task(MQTTManager(version_repo=version_repo, device_repo=device_repo, notification_repo=notification_repo, telemetry_repo=telemetry_repo, trigger_repo=trigger_repo).start())

    yield


init(dsn=getenv('SENTRY_DSN'))

app = FastAPI(title='Espartan API', version='v1', lifespan=lifespan)

app.include_router(AppVersionRouter(version_repo).router)
app.include_router(DeviceRouter(device_repo).router)
app.include_router(NotificationRouter().router)
app.include_router(RelayRouter(RelayRepository()).router)
app.include_router(SettingsRouter(SettingsRepository()).router)
app.include_router(TelemetryRouter(telemetry_repo).router)
app.include_router(TriggerRouter().router)

app.add_middleware(CORSMiddleware, expose_headers=['X-Total-Count'], allow_headers=['*'], allow_methods=['*'], allow_origins=['*'])

if app_config.environment != 'dev':
    app.mount('/web', SpaStaticFiles(directory=path.join(path.dirname(__file__), '..', 'web'), html=True), name='web')
