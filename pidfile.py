"""
Project: pylockfile
Module:pidfile.py
Description: Implementationo of pid file concepts.

Pid file it's like 'lock' for current process

Copyright 2023, Andrey Loginov
"""

__author__ = "Andrey Loginov"
__email__ = "andreyloginovmob@gmail.com"

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
    def get_pid(self)->str:
        """

        Just return Process Identificator
        :return:

        """
        return str(os.getpid())

    @staticmethod
    def _add_lock_extension(lockname: str) -> str:
        pid_name = f"{str(os.getpid())}.pid"
        return lockname + pid_name if not lockname.endswith(pid_name) else lockname

