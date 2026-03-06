class BaseBluetoothManager:
    def ensure_bluetooth_disabled(self) -> bool:
        raise NotImplementedError('Subclasses must implement this method')
