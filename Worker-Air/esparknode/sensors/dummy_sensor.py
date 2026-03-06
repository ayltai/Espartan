from esparknode.sensors.base_sensor import BaseSensor


class DummySensor(BaseSensor):
    def read(self) -> dict:
        return {
            'temperature' : 25.0,
            'humidity'    : 50.0,
        }
