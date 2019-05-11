
class Handler:
    def __init__(self, clickup_client):
        self.client = clickup_client

    def access(self, path: str, mode: int) -> None:
        return True

    def chmod(self, path: str, mode) -> None:
        pass

    def chown(self, path: str, uid, gid) -> None:
        pass

    def getattr(self, path:str, fh=None) -> dict:
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
        pass

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