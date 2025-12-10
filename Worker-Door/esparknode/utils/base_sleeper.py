class BaseSleeper:
    def light_sleep(self, duration: int) -> None:
        raise NotImplementedError('Subclasses must implement this method')

    def deep_sleep(self, duration: int) -> None:
        raise NotImplementedError('Subclasses must implement this method')
