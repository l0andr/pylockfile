"""
Project: pylockfile
Module:lockfile.py
Description: Implementation of lockfile concepts

Copyright 2023, Andrey Loginov
"""

import os
import uuid
from typing import Optional

from lock_exceptions import AlreadyLocked, IsNotLocked


class LockFile:
    """
        Base lockfile class 
    """
    default_file_name_length: int = 8

    def __init__(self, lockname: Optional[str] = None, lockfiledir: Optional[str] = None):
        """
        :param lockname: name of lockfile, if not specified will be generated random name
        :param lockfiledir: directory where lockfile should be placed, must exist, default: current directory
        """
        self.__lockname = lockname
        if not self.__lockname:
            self.__lockname = self._generate_default_lockname()
        self.lockfiledir = lockfiledir
        if not self.lockfiledir:
            self.lockfiledir = ""
        if self.lockfiledir and not os.path.isdir(self.lockfiledir):
            raise RuntimeError(f"{self.__class__.__name__}: Specified directory {lockfiledir} does not exists")

    @classmethod
    def _generate_default_lockname(cls) -> str:
        filename = ''
        while len(filename) < cls.default_file_name_length:
            if cls.default_file_name_length > 32:
                filename+=uuid.uuid4().hex[0:(31 - len(filename) + 1)]
            else:
                filename+=uuid.uuid4().hex[0:cls.default_file_name_length - 1]
        return filename

    @staticmethod
    def _add_lock_extension(lockname: str) -> str:
        return lockname + '.lock' if not lockname.endswith('.lock') else lockname

    def __get_lock_file_path(self):
        self.__lockfilename = self._add_lock_extension(self.__lockname)
        return os.path.join(self.lockfiledir, self.__lockfilename)

    def __create_lock_file(self):
        fid = open(self.__get_lock_file_path(), 'w')
        fid.close()
    @property
    def lockname(self):
        return self.__lockname
    def lock(self):
        """
        Set lock, raise exception (AlreadyLocked) in case, if it set already
        :return:
        """
        if os.path.exists(self.__get_lock_file_path()):
            raise AlreadyLocked()
        self.__create_lock_file()

    def release(self):
        """
        Release lock, raise exception (IsNotLocked) in case, if lock have not been set
        :return:
        """
        if not os.path.exists(self.__get_lock_file_path()):
            raise IsNotLocked()
        os.remove(self.__get_lock_file_path())

    def is_locked(self) -> bool:
        """
        Check is lock set.
        :return: bool
        """
        return os.path.exists(self.__get_lock_file_path())

    def __del__(self):
        if self.is_locked():
            self.release()
