"""
Project: pylockfile
Module:pidfile.py
Description: Implementationo of pid file concepts.

Pid file it's like 'lock' for current process

Copyright 2023, Andrey Loginov
"""

import os

import lockfile


class PidFile(lockfile.LockFile):
    """
    Implementation of pidfile concept
    """

    @classmethod
    def _generate_default_lockname(cls) -> str:
        lockname = 'pid_'
        return lockname

    @property
    def get_pid(self) -> str:
        """

        Just return Process Identificator
        :return:

        """
        return str(os.getpid())

    @staticmethod
    def _add_lock_extension(lockname: str) -> str:
        pid_name = f"{str(os.getpid())}.pid"
        return lockname + pid_name if not lockname.endswith(pid_name) else lockname


class SinglePidFile(PidFile):
    """
    Singleton version, have the same behaviour as PidFil, but can be created more than one object
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or cls.instance is None:
            cls.instance = super(SinglePidFile, cls).__new__(cls)
        return cls.instance
