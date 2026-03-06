from esparknode.networks.base_bluetooth import BaseBluetoothManager


class BluetoothManager(BaseBluetoothManager):
    def ensure_bluetooth_disabled(self) -> bool:
        return True
