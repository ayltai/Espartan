from pytest import fixture

from fastapi.testclient import TestClient

from src.main import app


@fixture
def client():
    return TestClient(app)


@fixture
def async_monkeypatch(monkeypatch):
    def _patch(target, value):
        async def wrapper(*args, **kwargs):
            return value(*args, **kwargs) if callable(value) else value

        monkeypatch.setattr(target, wrapper)

    return _patch


def test_relay_current_state(client, monkeypatch):
    async def async_get_current_state(self, session, device_id):
        return 1

    monkeypatch.setattr('src.routers.relay.RelayRepository.get_current_state', async_get_current_state)

    response = client.get('/api/v1/relays/current/dev1')

    assert response.status_code == 200
    assert response.json() == 1


def test_settings_get_by_id(client, monkeypatch):
    async def async_get(self, session, *args, **kwargs):
        return {
            'id' : 1,
        }

    monkeypatch.setattr('src.routers.settings.SettingsRepository.get', async_get)

    response = client.get('/api/v1/settings/1')

    assert response.status_code == 200
    assert response.json()['id'] == 1
