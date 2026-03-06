from os import path

from esparknode.data.base_storage import BaseStorage


class Storage(BaseStorage):
    FILE_PATH = '/tmp/espark.ini'

    def set_int(self, key: str, value: int) -> None:
        mappings = self._load() or {}
        mappings[key] = value

        self._save(mappings)

    def get_int(self, key: str) -> int | None:
        mappings = self._load()
        return None if mappings is None else mappings.get(key)

    def _load(self):
        mappings: dict[str, int] = {}

        if path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
                for line in file:
                    key, value = line.strip().split('=')

                    mappings[key] = int(value)

        return mappings

    def _save(self, mappings: dict[str, int]) -> None:
        with open(self.FILE_PATH, 'w', encoding='utf-8') as file:
            for key, value in mappings.items():
                file.write(f'{key}={value}\n')
