from pytest import fixture
from unittest.mock import MagicMock

from src.worker_node import WorkerNode


class DummyRelay:
    def __init__(self, pin=None):
        self.state = None

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False


@fixture
def worker_node(monkeypatch):
    sleeper           = MagicMock()
    watchdog          = MagicMock()
    wifi_manager      = MagicMock()
    mqtt_manager      = MagicMock()
    bluetooth_manager = MagicMock()

    return WorkerNode(
        device_id='dev1',
        sleeper=sleeper,
        watchdog=watchdog,
        wifi_manager=wifi_manager,
        mqtt_manager=mqtt_manager,
        bluetooth_manager=bluetooth_manager,
    )


def test_handle_parameters_update(worker_node):
    worker_node.sleep_interval = 123

    worker_node._handle_parameters_update({
        'sleep_interval' : 456,
    })

    assert worker_node.sleep_interval == 456
