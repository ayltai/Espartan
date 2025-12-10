from asyncio import create_task
from contextlib import asynccontextmanager
from os import path

from esparkcore.data.repositories import DeviceRepository, TelemetryRepository
from esparkcore.data import init_db
from esparkcore.routers import DeviceRouter, TelemetryRouter
from esparkcore.services import MQTTManager
from esparkcore.schedules import start_scheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .data.repositories import RelayRepository, SettingsRepository
from .data import init_settings
from .routers import RelayRouter, SettingsRouter
from .schedules import evaluate, process_outbox
from .utils import AppConfig

app_config     = AppConfig()
device_repo    = DeviceRepository()
telemetry_repo = TelemetryRepository()


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

    create_task(MQTTManager(device_repo, telemetry_repo).start())

    yield


app = FastAPI(title='Espartan API', version='v1', lifespan=lifespan)

app.include_router(DeviceRouter(device_repo).router)
app.include_router(RelayRouter(RelayRepository()).router)
app.include_router(SettingsRouter(SettingsRepository()).router)
app.include_router(TelemetryRouter(telemetry_repo).router)

app.add_middleware(CORSMiddleware, expose_headers=['X-Total-Count'], allow_headers=['*'], allow_methods=['*'], allow_origins=['*'])

if app_config.environment != 'dev':
    app.mount('/web', SpaStaticFiles(directory=path.join(path.dirname(__file__), '..', 'web'), html=True), name='web')
