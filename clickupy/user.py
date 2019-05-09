import json

from .handler import Handler

class UserHandler(Handler):
    def getattr(self, path:str, fh=None) -> dict:
        return {
            # time of last access
            "st_atime": 1557351945,
            # Time of last status change
            "st_ctime": 1557351945,
            # time of last modification
            "st_mtime": 1557351945,
            # Group that owns the file
            "st_gid": 20,
            # File or folder
            "st_mode": 33188,
            # Number of hard links
            "st_nlink": 1,
            # Size of file in bytes
            "st_size": 1024,
            # user id
            "st_uid": 501
        }
    def open(self, path: str, flags):
        return 1337

    def read(self, path: str, length: int, offset: int, fh):
        user = self.client.user()
        return bytes(json.dumps(user,indent=2))