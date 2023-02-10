"""
Project: pylockfile
Module:signal_dispatcher.py
Description: Contain class for adding and replacing handlers for POSIX processes signals

Copyright 2023, Andrey Loginov
"""

from typing import Callable, Optional, Any, Union
from types import FrameType
import signal


class SignalDispatcher:
    """
        Class for adding and replacing handlers for Posix processes signals
        Note: Limitation, in case if we need add 2 or more handlers to the same signal may be
        triky to not confused in order of call off 'add' and 'release' methods. Ideally it should be
        implemented as something like singelton with deque of calls
    """

    ###TODO implement SignalDispatcher class as singelton, store and call previous handlers from deque
    def __init__(self, sig: signal.Signals):
        """
        :param sig:  Should be some signal from signal.Signals (i.e signal.SIGTERM, signal.SIGINT etc)
        """

        self.__previous_handler: Union[Callable[[int, Optional[FrameType]], Any], int, None] = None
        self.__signal_handler: Union[Callable[[int, Optional[FrameType]], Any], int, None] = None
        self.__sig:signal.Signals = sig

    def set(self, signal_handler: Union[Callable[[int, Optional[FrameType]], Any], int, None]):
        """
        Set new handler for signal, old signal handler will be ignored
        :param signal_handler: callable - new handler for signal
        :return:
        """
        if self.__signal_handler is None:
            self.__signal_handler = signal_handler
            self.__previous_handler = signal.getsignal(self.__sig)
            signal.signal(self.__sig, signal_handler)
        else:
            raise RuntimeError(f"Signal handler was already set for signal {self.__sig}")

    def add(self, signal_handler: Union[Callable[[int, Optional[FrameType]], Any], int, None]):
        """
           Add new handler for signal, old handler will be called after new one
           :param signal_handler: callable - new handler for signal
           :return:
           """
        if self.__signal_handler is None:
            self.__signal_handler = signal_handler
            self.__previous_handler = signal.getsignal(self.__sig)
            def helper(*args, **kwargs):
                if callable(self.__signal_handler):
                    self.__signal_handler(*args, **kwargs)
                    if callable(self.__previous_handler):
                        self.__previous_handler(*args, **kwargs)

            signal.signal(self.__sig, helper)
        else:
            raise RuntimeError(f"Signal handler was already set for signal {self.__sig}")

    def restore(self):
        """
        Restore previous state of signal handler
        :return:
        """
        if self.__signal_handler is not None:
            self.__signal_handler = None
            if self.__previous_handler == signal.SIG_IGN or self.__previous_handler == signal.SIG_DFL or \
                    callable(self.__previous_handler):
                signal.signal(self.__sig, self.__previous_handler)
            self.__previous_handler = None
        else:
            raise RuntimeError(f"New signal handler was not set for signal {self.__sig}")

    def __del__(self):
        if self.__signal_handler is not None:
            self.restore()
