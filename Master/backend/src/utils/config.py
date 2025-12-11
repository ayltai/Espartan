from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE : str = '/opt/espartan/.env'


class AppConfig(BaseSettings):
    environment                 : str = 'dev'
    database_url                : str = 'sqlite+aiosqlite:///database.db'
    mqtt_host                   : str = 'localhost'
    mqtt_port                   : int = 1883
    slack_token                 : str = ''
    slack_channel               : str = ''
    device_sleep_interval       : int = 600
    heating_evaluation_interval : int = 10
    heating_evaluation_strategy : str = 'min'
    outbox_processing_interval  : int = 10

    model_config = SettingsConfigDict(
        env_file=ENV_FILE if path.exists(ENV_FILE) else '.env',
        env_file_encoding='utf-8',
    )
