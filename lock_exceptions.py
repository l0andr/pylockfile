"""
Project: pylockfile
Module:lock_exceptions.py
Description:

In this file are locks related exceptions

Copyright 2023, Andrey Loginov
"""

class PylockException(Exception):
    pass

class AlreadyLocked(PylockException):
    pass

class IsNotLocked(PylockException):
    pass

class WrapFuncNotDefined(PylockException):
    pass
