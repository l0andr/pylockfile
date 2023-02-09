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

def test_lockfile_lockname():
    lock = lockfile.LockFile(lockname="testlock",lockfiledir='.')
    lock.lock()
    assert lock.lockname == 'testlock'

def test_lockfile_as_ContextManager():
    lock = lockfile.LockFile(lockname="testlock", lockfiledir='.')
    with lock as lockname:
        assert lockname == 'testlock'
        assert os.path.exists('testlock.lock')
    assert not os.path.exists('testlock.lock')

def test_lockfile_as_decorator():
    @lockfile.LockFile(lockname='testdecorator')
    def some_func(A:int,B:int):
        assert os.path.exists('testdecorator.lock')
        return A*B
    A = 5
    B = 7
    assert some_func(A,B) == A*B
    assert not os.path.exists('testdecorator.lock')

