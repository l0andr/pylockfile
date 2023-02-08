import os.path

import pytest
import pidfile
from lock_exceptions import AlreadyLocked,IsNotLocked

def test_pidfile_lock():
    lock = pidfile.PidFile()
    lock.lock()
    assert os.path.exists(f'pid_{os.getpid()}.pid')
    double_lock_failed = False
    try:
        lock.lock()
    except AlreadyLocked:
        double_lock_failed = True
    assert double_lock_failed
