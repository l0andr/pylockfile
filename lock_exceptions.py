"""
Project: pylockfile
Module:lock_exceptions.py
Description:

In this file are locks related exceptions

Copyright 2023, Andrey Loginov
"""

class PylockException(Exception):
    """
    Base class for all pylockfile exceptions
    """
class AlreadyLocked(PylockException):
    """
    Exception will rise on attempt to lock already locked object
    """
class IsNotLocked(PylockException):
    """
    Exception will rise on attempt to unlock not locked object
    """
class WrapFuncNotDefined(PylockException):
    """
    Exception will rise on attempt call unwrapped function
    """
