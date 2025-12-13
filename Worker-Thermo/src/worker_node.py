from esparknode.actions.base_relay import BaseRelay
from esparknode.base_node import BaseNode
from esparknode.networks.base_bluetooth import BaseBluetoothManager
from esparknode.networks.base_mqtt import BaseMQTTManager
from esparknode.networks.base_wifi import BaseWiFiManager
from esparknode.sensors.base_sensor import BaseSensor
from esparknode.triggers.base_trigger import BaseTrigger
from esparknode.utils.base_sleeper import BaseSleeper
from esparknode.utils.base_watchdog import BaseWatchdog
from esparknode.utils.logging import log_debug


class WorkerNode(BaseNode):
    def __init__(
            self,
            device_id         : str,
            sleeper           : BaseSleeper,
            watchdog          : BaseWatchdog,
            wifi_manager      : BaseWiFiManager,
            mqtt_manager      : BaseMQTTManager,
            bluetooth_manager : BaseBluetoothManager = None,
            actions           : list[BaseRelay]      = None,
            sensors           : list[BaseSensor]     = None,
            triggers          : list[BaseTrigger]    = None,
    ):
        super().__init__(
            device_id=device_id,
            sleeper=sleeper,
            watchdog=watchdog,
            wifi_manager=wifi_manager,
            mqtt_manager=mqtt_manager,
            bluetooth_manager=bluetooth_manager,
            sensors=sensors,
            triggers=triggers,
        )

        self.actions = actions if actions is not None else []

    def _handle_parameters_update(self, parameters: dict) -> None:
        self.sleep_interval = parameters.get('sleep_interval', self.sleep_interval)

        super()._handle_parameters_update(parameters)

    def _handle_action(self, payload: dict) -> None:
        state : bool = payload['state'] == 1

        log_debug(f'Setting relay state to: {state}')

        for action in self.actions:
            if state:
                action.turn_on()
            else:
                action.turn_off()

            self.watchdog.feed()
