class BaseTrigger:
    def __init__(self, trigger_type: str, name: str = None):
        self.trigger_type = trigger_type
        self.name         = name
        self.callbacks    = []

    def get_type(self) -> str:
        return self.trigger_type

    def get_name(self) -> str:
        return self.name

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def start(self):
        raise NotImplementedError('Start method must be implemented by subclasses.')

    def stop(self):
        raise NotImplementedError('Stop method must be implemented by subclasses.')
