class BaseSensor:
    def read(self) -> dict:
        raise NotImplementedError('Subclasses must implement this method')
