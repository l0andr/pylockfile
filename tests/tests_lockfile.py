#pylint: disable=missing-module-docstring
#pylint: disable-next=missing-function-docstring

import os.path
import signal

import pytest # pylint: disable=unused-import
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
    lock.release()
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
    lock.release()
def test_lockfile_as_context_manager():
    lock = lockfile.LockFile(lockname="testlock", lockfiledir='.')
    with lock as lockname:
        assert lockname == 'testlock'
        assert os.path.exists('testlock.lock')
    assert not os.path.exists('testlock.lock')

def test_lockfile_as_decorator():
    @lockfile.LockFile(lockname='testdecorator')
    def some_func(a_v:int,b_v:int):
        assert os.path.exists('testdecorator.lock')
        return a_v*b_v
    a_v = 5
    b_v = 7
    assert some_func(a_v,b_v) == a_v*b_v
    assert not os.path.exists('testdecorator.lock')

def test_lockfile_with_sigint_handler():

    lock = lockfile.LockFile(lockname="testlock", lockfiledir='.',delete_lock_on_sigint=True)
    lock.lock()
    assert lock.is_locked()
    keyboard_interrupt_was_raised = False
    try:
        os.kill(os.getpid(), signal.SIGINT)
    except KeyboardInterrupt:
        keyboard_interrupt_was_raised = True
    assert not lock.is_locked()
    assert keyboard_interrupt_was_raised

