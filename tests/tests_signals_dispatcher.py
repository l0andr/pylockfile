#pylint: disable=missing-module-docstring
#pylint: disable-next=missing-function-docstring

import signal
import os

import pytest # pylint: disable=unused-import
import signals_dispatcher

def test_set_signal_handler():
    sig_usr1 = signals_dispatcher.SignalDispatcher(signal.SIGUSR1)
    global D #pylint: disable=global-variable-undefined
    D = None
    def test_handler(sig,frame): #pylint: disable=unused-argument
        global D #pylint: disable=global-variable-undefined
        D = sig
    sig_usr1.set(test_handler)
    os.kill(os.getpid(), signal.SIGUSR1)
    assert D == signal.SIGUSR1
    sig_usr1.restore()


def test_add_signal_handler():
    sig_int = signals_dispatcher.SignalDispatcher(signal.SIGINT)
    global D  # pylint: disable=global-variable-undefined
    D = None
    def test_handler(sig, frame):  # pylint: disable=unused-argument
        global D  # pylint: disable=global-variable-undefined
        D = sig
    sig_int.add(test_handler)
    keyboard_interrupt_was_raised = False
    try:
        os.kill(os.getpid(), signal.SIGINT)
    except KeyboardInterrupt:
        keyboard_interrupt_was_raised = True
    assert D == signal.SIGINT
    assert keyboard_interrupt_was_raised
    sig_int.restore()
    D -= 1
    keyboard_interrupt_was_raised = False
    try:
        os.kill(os.getpid(), signal.SIGINT)
    except KeyboardInterrupt:
        keyboard_interrupt_was_raised = True
    assert keyboard_interrupt_was_raised
    assert D == signal.SIGINT - 1


