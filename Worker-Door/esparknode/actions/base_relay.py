class BaseRelay:
    def turn_on(self):
        raise NotImplementedError('This method should be overridden by subclasses.')

    def turn_off(self):
        raise NotImplementedError('This method should be overridden by subclasses.')

    def toggle(self):
        pass

    def get_state(self) -> int | None:
        pass
