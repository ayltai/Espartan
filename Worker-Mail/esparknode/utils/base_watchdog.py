class BaseWatchdog:
    def feed(self):
        raise NotImplementedError('Subclasses must implement this method')
