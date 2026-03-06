class BaseStorage:
    def set_int(self, key: str, value: int) -> None:
        raise NotImplementedError('Subclasses must implement this method')

    def get_int(self, key: str) -> int | None:
        raise NotImplementedError('Subclasses must implement this method')
