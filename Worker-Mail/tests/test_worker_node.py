from pytest import fixture
from unittest.mock import MagicMock

import esparknode.configs

from esparknode.triggers.base_trigger import BaseTrigger

from src.worker_node import WorkerNode

class DummyTrigger(BaseTrigger):
    def __init__(self):
        super().__init__('mail_in', 'mail')

        self.callbacks = []
        self.started = False
        self.stopped = False

    def register_callback(self, cb):
        self.callbacks.append(cb)

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

@fixture
def worker_node(monkeypatch):
    sleeper           = MagicMock()
    watchdog          = MagicMock()
    wifi_manager      = MagicMock()
    mqtt_manager      = MagicMock()
    bluetooth_manager = MagicMock()
    triggers          = [DummyTrigger()]

    return WorkerNode(
        device_id='dev1',
        sleeper=sleeper,
        watchdog=watchdog,
        wifi_manager=wifi_manager,
        mqtt_manager=mqtt_manager,
        bluetooth_manager=bluetooth_manager,
        triggers=triggers,
    )

def test_on_triggered_publishes_telemetry(worker_node):
    trigger = worker_node.triggers[0]

    worker_node.mqtt_manager.publish = MagicMock()
    worker_node._on_triggered(True, trigger)

    worker_node.mqtt_manager.publish.assert_called()
    args, kwargs = worker_node.mqtt_manager.publish.call_args

    assert worker_node.device_id in args[0]
    assert 'mail' in args[1] or 'data_type' in args[1]
