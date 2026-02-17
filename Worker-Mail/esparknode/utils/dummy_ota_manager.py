from esparknode.utils.base_ota_manager import BaseOtaManager


class OtaManager(BaseOtaManager):
    def apply(self, manifest: str) -> None:
        print(f'Applying OTA update with manifest: {self.base_url}/{manifest}')
