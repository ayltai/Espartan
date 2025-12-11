from esparkcore.notifications.slack_notifier import SlackNotifier
from esparkcore.services.mqtt import MQTTManager

from ..utils import AppConfig


class ReactiveMQTTManager(MQTTManager):
    async def _handle_telemetry(self, device_id: str, payload: dict) -> None:
        await super()._handle_telemetry(device_id, payload)

        if payload.get('data_type') == 'door_open' and payload.get('value') >= 100:
            config = AppConfig()

            if config.slack_token and config.slack_channel:
                await SlackNotifier(slack_token=config.slack_token, slack_channel=config.slack_channel).notify(device_id=device_id, event_type=payload.get('data_type'), value=payload.get('value') / 100)
