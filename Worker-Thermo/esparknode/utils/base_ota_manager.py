from esparknode.networks.base_requests import BaseRequests


class BaseOtaManager:
    def __init__(self, requests: BaseRequests):
        self.requests = requests

    def apply(self, manifest: str) -> None:
        raise NotImplementedError('decompress_and_apply method must be implemented by subclasses')
