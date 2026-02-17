# pylint: disable=no-name-in-module
from os import ilistdir, listdir, mkdir, remove, rename, rmdir, stat

# pylint: disable=import-error
from machine import reset
# pylint: disable=import-error
from mip import install

from esparknode.utils.base_ota_manager import BaseOtaManager
from esparknode.utils.logging import log_error

S_IFDIR : int = 0x4000
S_IFREG : int = 0x8000

OTA_DIR : str = '/ota'


def rmtree(path):
    try:
        for entry in ilistdir(path):
            name = entry[0]
            full = path + "/" + name

            if entry[1] == S_IFDIR:
                rmtree(full)
            else:
                remove(full)

        rmdir(path)
    except OSError as e:
        log_error(e)


def ensure_clean_dir(path):
    try:
        rmtree(path)
    # pylint: disable=broad-exception-caught
    except Exception:
        pass

    try:
        mkdir(path)
    # pylint: disable=broad-exception-caught
    except Exception:
        pass


class OtaManager(BaseOtaManager):
    def apply(self, manifest: str) -> None:
        ensure_clean_dir(OTA_DIR)

        install(f'{self.base_url}{manifest}', target=OTA_DIR, mpy=False)

        # Deletes everything in '/' except 'boot.py' and '/ota'.
        for item in listdir('/'):
            if item not in ['boot.py', 'ota']:
                item_path = '/' + item

                try:
                    mode = stat(item_path)[0]
                    if mode & S_IFREG == S_IFREG:
                        remove(item_path)
                    elif mode & S_IFDIR == S_IFDIR:
                        rmtree(item_path)
                # pylint: disable=broad-exception-caught
                except Exception as e:
                    log_error(e)

        # Moves everything from '/ota' to '/'.
        for item in listdir(OTA_DIR):
            item_path = OTA_DIR + '/' + item
            dest_path = '/' + item

            try:
                mode = stat(item_path)[0]
                if mode & S_IFREG == S_IFREG:
                    rename(item_path, dest_path)
                elif mode & S_IFDIR == S_IFDIR:
                    rename(item_path, dest_path)
            # pylint: disable=broad-exception-caught
            except Exception as e:
                log_error(e)

        reset()
