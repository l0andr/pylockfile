import os.path

import pytest
import lockfile
from lock_exceptions import AlreadyLocked,IsNotLocked

def test_lockfile_init():
    lock = lockfile.LockFile()
    assert isinstance(lock,lockfile.LockFile)

def test_lockfile_lock():
    lock = lockfile.LockFile()
    lock.lock()
    double_lock_failed = False
    try:
        lock.lock()
    except AlreadyLocked:
        double_lock_failed = True
    assert double_lock_failed

def test_lockfile_release():
    lock = lockfile.LockFile()
    first_release_failed = False
    try:
        lock.release()
    except IsNotLocked:
        first_release_failed = True
    assert first_release_failed
    lock.lock()
    lock.release()
    assert not lock.is_locked()

def test_lockfile_lock_named():
    lock = lockfile.LockFile(lockname="testlock",lockfiledir='.')
    lock.lock()
    assert os.path.exists('testlock.lock')
    lock.release()
    assert not os.path.exists('testlock.lock')