# pylint: disable=import-error
from bluetooth import BLE

from esparknode.networks.base_bluetooth import BaseBluetoothManager


class BluetoothManager(BaseBluetoothManager):
    def ensure_bluetooth_disabled(self) -> bool:
        ble = BLE()
        ble.active(False)

        return not ble.active()
