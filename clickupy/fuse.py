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

from .handler import *

class Router:
    """
    A router that matches filesystem operations at a given path
    to a handler
    """
    def __init__(self, client):
        self.client = client
        self.handlers = [
            (r"^/$", BaseHandler(client)),
            (r"^/user$", UserHandler(client)),
            (r"^/teams\/?$", TeamsHandler(client)),
            (r"^/teams/[0-9]+$", TeamHandler(client))

        ]

    def match(self, operation: str, path: str):
        """
        Determine if a handler existers for the operation
        at a given path
        """
        for reg, handler in self.handlers:
            if re.match(reg, path):
                print("Found matching handler for", operation, path)
                method = getattr(handler, operation)
                return method
        raise Exception(f"No handler for {operation} at {path}")
 
def delegate(func):
    """
    Decorator that delegates execution of a FUSE callback to
    the appropriate handler.
    """
    @functools.wraps(func)
    def wrapped(self, *args, **kwargs):
        path = args[0]
        handler = self.router.match(func.__name__, path)
        return handler(*args, **kwargs)
    return wrapped

class ClickupFS(LoggingMixIn):
    """A FUSE filesystem for Clickup"""
    def __init__(self, root: str, clickup_client):
        self.root = root
        self.client = clickup_client
        self.router = Router(self.client)

    # Filesystem methods

    @log
    @delegate
    def access(self, path: str, mode: int) -> None:
        pass

    @log
    @delegate
    def chmod(self, path: str, mode) -> None:
        pass

    @log
    @delegate
    def chown(self, path: str, uid, gid) -> None:
        pass

    @log
    @delegate
    def getattr(self, path:str, fh=None) -> dict:
        pass

    @log
    @delegate
    def readdir(self, path: str, fh: int) -> list:
        pass

    @log
    @delegate
    def readlink(self, path: str):
        pass

    @log
    @delegate
    def mknod(self, path, mode, dev):
        pass

    @log
    @delegate
    def rmdir(self, path: str):
        pass

    @log
    @delegate
    def mkdir(self, path, mode):
        pass

    @log
    @delegate
    def statfs(self, path):
        #https://linux.die.net/man/2/statvfs
        pass

    @log
    @delegate
    def unlink(self, path):
        pass

    @log
    @delegate
    def symlink(self, name, target):
        pass

    @log
    @delegate
    def rename(self, old, new):
        pass

    @log
    @delegate
    def link(self, target, name):
        pass

    @log
    @delegate
    def utimens(self, path, times=None):
        pass

    # File methods
    @log
    @delegate
    def open(self, path, flags):
        pass

    @log
    @delegate
    def create(self, path, mode, fi=None):
        pass

    @log
    @delegate
    def read(self, path, length, offset, fh):
        pass

    @log
    @delegate
    def write(self, path, buf, offset, fh):
        pass

    @log
    @delegate
    def truncate(self, path, length, fh=None):
        pass

    @log
    @delegate
    def flush(self, path, fh):
        pass

    @log
    @delegate
    def release(self, path, fh):
        pass

    @log
    @delegate
    def fsync(self, path, fdatasync, fh):
        pass

def clickup_fuse(mountpoint: str, clickup_client):
    """Create a fuse filesystem for the clickup api"""
    return FUSE(ClickupFS(mountpoint, clickup_client), mountpoint, nothreads=True, foreground=True)
