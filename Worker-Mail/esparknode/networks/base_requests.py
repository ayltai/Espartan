class BaseRequests:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get(self, url: str) -> dict[str, int | str | None]:
        raise NotImplementedError('Subclasses must implement this method')
