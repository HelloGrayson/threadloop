from __future__ import absolute_import


class ThreadLoopException(Exception):
    pass


class ThreadNotStartedError(ThreadLoopException):
    pass
