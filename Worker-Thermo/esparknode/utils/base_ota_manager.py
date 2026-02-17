class BaseOtaManager:
    def __init__(self, base_url: str = None) -> None:
        self.base_url: str = base_url

    def apply(self, manifest: str) -> None:
        raise NotImplementedError('apply method must be implemented by subclasses')
