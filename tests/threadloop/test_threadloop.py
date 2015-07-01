from __future__ import absolute_import

import pytest

from concurrent.futures import Future
from threadloop import ThreadLoop
from tornado import gen


def test_coroutine_returns_future():

    @gen.coroutine
    def coroutine():
        raise gen.Return("Hello World")

    with ThreadLoop() as threadloop:
        future = threadloop.submit(coroutine)

        assert (
            isinstance(future, Future),
            "expected a concurrent.futures.Future"
        )

        assert future.result() == "Hello World"


def test_coroutine_exception_propagates():

    class TestException(Exception):
        pass

    @gen.coroutine
    def coroutine():
        raise TestException()

    with ThreadLoop() as threadloop:

        with pytest.raises(TestException):
            future = threadloop.submit(coroutine)
            future.result()
