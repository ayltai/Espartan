from requests import get as http_get

from esparknode.networks.base_requests import BaseRequests


class Requests(BaseRequests):
    def get(self, url: str) -> dict[str, bytes | int | str | None]:
        response = http_get(f'{self.base_url}{url}')

        return {
            'status_code' : response.status_code,
            'content'     : response.content,
            'text'        : response.text,
            'error'       : None if response.ok else response.reason,
        }
