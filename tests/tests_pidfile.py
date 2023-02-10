#pylint: disable=missing-module-docstring
#pylint: disable-next=missing-function-docstring

import os.path

import pytest # pylint: disable=unused-import
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

def test_pidfile_release():
    lock = pidfile.PidFile()
    release_failed = False
    try:
        lock.release()
    except IsNotLocked:
        release_failed = True
    assert release_failed

def test_pidfile_as_context_manager():
    with pidfile.PidFile('test_') as lockname:
        assert os.path.exists(f'{lockname}{os.getpid()}.pid')
        pid_obj = pidfile.PidFile('test_')
        double_lock_failed = False
        try:
            pid_obj.lock()
        except AlreadyLocked:
            double_lock_failed = True
        assert double_lock_failed
    assert not os.path.exists(f'test_{os.getpid()}.pid')

def test_singlepidfile_as_singleton():
    spf =  pidfile.SinglePidFile('test_')
    spf2 = pidfile.SinglePidFile('test2_')
    mpf = pidfile.PidFile('test2_')
    assert mpf.lockname == 'test2_'
    assert spf2.lockname == 'test_'
    assert spf == spf2
    assert spf.lockname == spf2.lockname


def test_singlepidfile_as_context_manager():
    with pidfile.SinglePidFile('test_') as lockname:
        spf = pidfile.SinglePidFile()
        assert spf.lockname == lockname
        assert spf.is_locked()
    spf = pidfile.SinglePidFile()
    assert not spf.is_locked()