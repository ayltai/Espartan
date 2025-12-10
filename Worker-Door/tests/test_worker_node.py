from pytest import fixture
from unittest.mock import MagicMock

import esparknode.configs

from esparknode.triggers.base_trigger import BaseTrigger

from src.worker_node import WorkerNode


class DummyTrigger(BaseTrigger):
    def __init__(self):
        super().__init__('ld2420', 'motion')

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

def test_handle_parameters_update(worker_node):
    params = {
        'sleep_interval'         : 123,
        'max_detection_duration' : 456,
        'detection_enabled'      : False,
    }

    worker_node._handle_parameters_update(params)

    assert worker_node.sleep_interval == 123
    assert worker_node.max_detection_duration == 456
    assert worker_node.detection_enabled is False

def test_on_triggered_publishes_mqtt(worker_node):
    mqtt_manager = worker_node.mqtt_manager
    mqtt_manager.publish = MagicMock()

    worker_node._on_triggered(True, worker_node.triggers[0])

    calls = mqtt_manager.publish.call_args_list
    assert any('motion' in str(call) for call in calls)

def test_publish_telemetry_calls_mqtt_and_detection(worker_node, monkeypatch):
    mqtt_manager = worker_node.mqtt_manager
    mqtt_manager.publish = MagicMock()

    worker_node.start_detection = MagicMock()

    worker_node.publish_telemetry()

    assert mqtt_manager.publish.called
    assert worker_node.start_detection.called

def test_start_buzzer_and_stop_buzzer(worker_node, monkeypatch):
    esparknode.configs.ENVIRONMENT = 'unix'

    worker_node.buzzer_started = False

    worker_node.start_buzzer()

    assert worker_node.buzzer_started is True

    worker_node.stop_buzzer()

    assert worker_node.buzzer_started is False
