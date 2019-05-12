import json

import functools

from .handler import Handler

def log(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        print(f"{func.__name__.upper()} with {args}, {kwargs}")
        ret = func(self, *args, **kwargs)
        print("Returned", ret)
        return ret
    return inner

class UserHandler(Handler):
    @log
    def getattr(self, path: str, fh: int = None) -> dict:
        user = self.client.user()
        data = bytes(json.dumps(user,indent=2), "utf8")
        return {
            # time of last access
            "st_atime": 1557351945,
            # Time of last status change
            "st_ctime": 1557351945,
            # time of last modification
            "st_mtime": 1557351945,
            # Group that owns the file
            "st_gid": 0,
            # File or folder
            "st_mode": 33188,
            # Number of hard links
            "st_nlink": 1,
            # Size of file in bytes
            "st_size": len(data),
            # user id
            "st_uid": 501
        }

    @log
    def open(self, path: str, flags):
        return 0

    @log
    def read(self, path: str, length: int, offset: int, fh: int):
        user = self.client.user()
        data = bytes(json.dumps(user,indent=2), "utf8")
        return data[offset:offset+length]