# pylint: disable=import-error
from esp32 import NVS

from esparknode.data.base_storage import BaseStorage


class Storage(BaseStorage):
    def __init__(self):
        self.nvs = NVS('app')

    def set_int(self, key: str, value: int) -> None:
        self.nvs.set_i32(key, value)
        self.nvs.commit()

    def get_int(self, key: str) -> int | None:
        try:
            return self.nvs.get_i32(key)
        except OSError:
            return None
