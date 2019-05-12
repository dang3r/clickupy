
class Handler:
    def __init__(self, clickup_client):
        self.client = clickup_client

    def access(self, path: str, mode: int) -> None:
        return None

    def chmod(self, path: str, mode) -> None:
        return None

    def chown(self, path: str, uid, gid) -> None:
        return None

    def getattr(self, path:str, fh=None) -> dict:
        """
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
        """
        pass

    def readdir(self, path: str, fh: int) -> list:
        pass

    def readlink(self, path: str):
        pass

    def mknod(self, path, mode, dev):
        pass

    def rmdir(self, path):
        pass

    def mkdir(self, path, mode):
        pass

    def statfs(self, path: str):
        return {
            "f_bsize": 1048576,
            "f_frsize": 4096,
            "f_blocks": 1220613,
            "f_bfree": 760260,
            "f_bavail": 750614,
            "f_files": 42949672,
            "f_ffree": 42928496,
            "f_favail": 42928496,
            "f_flag": 0,
            "f_namemax": 255
        }

    def unlink(self, path: str):
        pass

    def symlink(self, name, target):
        pass

    def rename(self, old: str, new: str):
        pass

    def link(self, target, name):
        pass

    def utimens(self, path: str, times=None):
        pass

    # File methods
    # ============

    def open(self, path: str, flags):
        pass

    def create(self, path: str, mode, fi=None):
        pass

    def read(self, path: str, length: int, offset: int, fh):
        pass

    def write(self, path: str, buf, offset: str, fh):
        pass

    def truncate(self, path:str , length, fh=None):
        pass

    def flush(self, path: str, fh):
        pass

    def release(self, path: str, fh):
        pass

    def fsync(self, path: str, fdatasync, fh):
        pass