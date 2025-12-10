from pytest import fixture
from unittest.mock import MagicMock

from esparknode.sensors.base_sensor import BaseSensor

from src.worker_node import WorkerNode


class DummyRelay:
    def __init__(self, pin=None):
        self.state = None

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False


class DummySensor(BaseSensor):
    def __init__(self, data):
        self._data = data

    def read(self):
        return self._data


@fixture
def worker_node(monkeypatch):
    sleeper           = MagicMock()
    watchdog          = MagicMock()
    wifi_manager      = MagicMock()
    mqtt_manager      = MagicMock()
    bluetooth_manager = MagicMock()
    sensors           = [DummySensor({'temperature': 25, 'humidity': 50})]

    return WorkerNode(
        device_id='dev1',
        sleeper=sleeper,
        watchdog=watchdog,
        wifi_manager=wifi_manager,
        mqtt_manager=mqtt_manager,
        bluetooth_manager=bluetooth_manager,
        sensors=sensors,
    )


def test_handle_parameters_update(worker_node):
    worker_node.sleep_interval = 123

    worker_node._handle_parameters_update({
        'sleep_interval' : 456,
    })

    assert worker_node.sleep_interval == 456


def test_publish_telemetry(worker_node):
    mqtt_manager = worker_node.mqtt_manager
    mqtt_manager.publish = MagicMock()

    worker_node.publish_telemetry()

    calls = mqtt_manager.publish.call_args_list
    assert any('temperature' in str(call) for call in calls)
    assert any('humidity' in str(call) for call in calls)
