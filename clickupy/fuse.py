#!/usr/bin/env python3

from __future__ import with_statement

from abc import ABC, abstractmethod
import os
import logging
import sys
import errno
import functools
import re

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

logger = logging.getLogger('fuse.log-mixin')
logger.setLevel(logging.DEBUG)

from .user import UserHandler
from .base import BaseHandler

class Router:
    def __init__(self, client):
        self.client = client
        self.handlers = [
            (r"^/$", BaseHandler(client)),
            (r"^/user$", UserHandler(client))
        ]

    def match(self, operation, path):
        for reg, handler in self.handlers:
            if re.match(reg, path):
                print("Found matching handler for", operation, path)
                method = getattr(handler, operation)
                return method
        raise Exception("bad")


def log(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        print(f"{func.__name__.upper()} with {args}, {kwargs}")
        ret = func(self, *args, **kwargs)
        print("Returned", ret)
        return ret
    return inner

class ClickupFS(LoggingMixIn):
    def __init__(self, root: str, clickup_client):
        self.root = root
        self.client = clickup_client
        self.router = Router(self.client)

    # Filesystem methods
    # ==================

    @log
    def access(self, path: str, mode: int) -> None:
        return True

    @log
    def chmod(self, path: str, mode) -> None:
        return None

    @log
    def chown(self, path: str, uid, gid) -> None:
        return None

    @log
    def getattr(self, path:str, fh=None) -> dict:
        try:
            handler = self.router.match("getattr", path)
            return handler(path, fh)
        except:
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

    @log
    def readdir(self, path: str, fh: int) -> list:
        handler = self.router.match("readdir", path)
        return handler(path, fh)

    @log
    def readlink(self, path: str):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    @log
    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    @log
    def rmdir(self, path: str):
        pass


    @log
    def mkdir(self, path, mode):
        pass
        return os.mkdir(self._full_path(path), mode)

    @log
    def statfs(self, path):
        #https://linux.die.net/man/2/statvfs
        return {
            "f_bsize": 1048576,
            "f_frsize": 4096,
            "f_blocks": 122061322,
            "f_bfree": 76026015,
            "f_bavail": 75061489,
            "f_files": 4294967295,
            "f_ffree": 4292849674,
            "f_favail": 4292849674,
            "f_flag": 0,
            "f_namemax": 255
        }

        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    @log
    def unlink(self, path):
        return os.unlink(self._full_path(path))

    @log
    def symlink(self, name, target):
        return os.symlink(name, self._full_path(target))

    @log
    def rename(self, old, new):
        pass
        return os.rename(self._full_path(old), self._full_path(new))

    @log
    def link(self, target, name):
        return os.link(self._full_path(target), self._full_path(name))

    @log
    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        handler = self.router.match("readdir", path)
        return handler(path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

def clickup_fuse(mountpoint: str, clickup_client):
    """Create a fuse filesystem for the clickup api"""
    return FUSE(ClickupFS("/tmp", clickup_client), mountpoint, nothreads=True, foreground=True)
