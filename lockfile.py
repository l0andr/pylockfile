"""
Project: pylockfile
Module:lockfile.py
Description: Implementation of lockfile concepts

Copyright 2023, Andrey Loginov
"""

import os
import signal
import uuid
from typing import Optional, Callable
from functools import wraps
import lock_exceptions
import signals_dispatcher
class LockFile:
    """
        Base lockfile class
    """

    default_file_name_length: int = 8
    __lockname = None
    __lockfiledir = None
    __sig_term = None
    __sig_int = None

    def __init__(self, lockname: Optional[str] = None, lockfiledir: Optional[
        str] = None,delete_lock_on_sigterm = False, delete_lock_on_sigint = False):
        """
        :param lockname: name of lockfile, if not specified will be generated random name
        :param lockfiledir: directory where lockfile should be placed, must exist, default: current directory
        :param delete_lock_on_sigterm; If True lock will be release on SIGTERM signal [default True]
        :param delete_lock_on_sigint; If True lock will be release on SIGINT signal [default True]
        """
        if self.lockname is None:
            self.__lockname = lockname
        self.__lockfilename = None
        if not self.__lockname:
            self.__lockname = self._generate_default_lockname()
        if self.lockname is None:
            self.__lockfiledir = lockfiledir
        if not self.__lockfiledir:
            self.__lockfiledir = ""
        if self.__lockfiledir and not os.path.isdir(self.__lockfiledir):
            raise RuntimeError(f"{self.__class__.__name__}: Specified directory {lockfiledir} does not exists")
        if delete_lock_on_sigterm or delete_lock_on_sigint:
            def sigterm_handler(sig, frame): #pylint: disable=unused-argument
                if self.is_locked():
                    self.release()
            if delete_lock_on_sigterm:
                self.__sig_term = signals_dispatcher.SignalDispatcher(signal.SIGTERM)
                self.__sig_term.add(sigterm_handler)
            if delete_lock_on_sigint:
                self.__sig_int = signals_dispatcher.SignalDispatcher(signal.SIGINT)
                self.__sig_int.add(sigterm_handler)

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
        return os.path.join(self.__lockfiledir, self.__lockfilename)

    def __create_lock_file(self):
        with open(self.__get_lock_file_path(), 'w',encoding='utf8'):
            pass
    @property
    def lockname(self)->Optional[str]:
        """
        return lockname
        :return:
        """
        return self.__lockname

    def lock(self):
        """
        Set lock, raise exception (AlreadyLocked) in case, if it set already
        :return:
        """
        if os.path.exists(self.__get_lock_file_path()):
            raise lock_exceptions.AlreadyLocked()
        self.__create_lock_file()

    def release(self):
        """
        Release lock, raise exception (IsNotLocked) in case, if lock have not been set
        :return:
        """
        if not os.path.exists(self.__get_lock_file_path()):
            raise lock_exceptions.IsNotLocked()
        os.remove(self.__get_lock_file_path())

    def is_locked(self) -> bool:
        """
        Check is lock set.
        :return: bool
        """
        return os.path.exists(self.__get_lock_file_path())
    def __call__(self,wrappedfun:Callable):
        @wraps(wrappedfun)
        def wrapper(*args,**kwargs):
            self.lock()
            ans = wrappedfun(*args,**kwargs)
            self.release()
            return ans
        return wrapper
    def __enter__(self):
        self.lock()
        return self.__lockname

    def __exit__(self, type, value, traceback):
        self.release()

    def __del__(self):
        if self.is_locked():
            self.release()
