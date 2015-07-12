from __future__ import absolute_import


# All exceptions & errors inherit from this base exception.
class ThreadLoopException(Exception):
    pass


# Attempted to submit coroutine before ThreadLoop.start() was called.
class ThreadNotStartedError(ThreadLoopException):
    pass
