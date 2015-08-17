from __future__ import absolute_import
from decimal import Decimal
import time
from types import TracebackType
import traceback
import sys

import pytest

from concurrent.futures import Future, as_completed, TimeoutError
from threadloop import ThreadLoop
from threadloop.exceptions import ThreadNotStartedError
from tornado import gen, ioloop


@pytest.yield_fixture
def threadloop():
    with ThreadLoop() as threadloop:
        yield threadloop


class TestException(Exception):
    pass


def test_coroutine_returns_future(threadloop):

    @gen.coroutine
    def coroutine():
        raise gen.Return("Hello World")

    future = threadloop.submit(coroutine)

    assert (
        isinstance(future, Future),
        "expected a concurrent.futures.Future"
    )

    assert future.result() == "Hello World"


def test_propogates_arguments(threadloop):

    @gen.coroutine
    def coroutine(message, adjective="Shady"):
        raise gen.Return("Hello %s %s" % (adjective, message))

    future = threadloop.submit(coroutine, "World")
    assert future.result() == "Hello Shady World"

    future = threadloop.submit(coroutine, "World", adjective="Cloudy")
    assert future.result() == "Hello Cloudy World"


def test_coroutine_exception_propagates(threadloop):

    @gen.coroutine
    def coroutine():
        raise TestException()

    with pytest.raises(TestException):
        future = threadloop.submit(coroutine)
        future.result()


def test_coroutine_exception_contains_exc_info(threadloop):

    @gen.coroutine
    def coroutine():
        raise TestException('something went wrong')

    try:
        threadloop.submit(coroutine).result()
    except Exception:
        e, tb = sys.exc_info()[1:]

        assert isinstance(e, TestException)
        assert isinstance(tb, TracebackType)

        tb_out = traceback.extract_tb(tb)
        assert "raise TestException('something went wrong')" in str(tb_out)

        return

    assert False, "should have thrown exception"


def test_plain_function(threadloop):

    def not_a_coroutine():
        return "Hello World"

    future = threadloop.submit(not_a_coroutine)

    assert (
        isinstance(future, Future),
        "expected a concurrent.futures.Future"
    )

    assert future.result() == "Hello World"


def test_plain_function_exception_propagates(threadloop):

    def not_a_coroutine():
        raise TestException()

    future = threadloop.submit(not_a_coroutine)

    with pytest.raises(TestException):
        future = threadloop.submit(not_a_coroutine)
        future.result()


def test_plain_function_exception_contains_exc_info(threadloop):

    def not_a_coroutine():
        raise TestException('something went wrong')

    try:
        threadloop.submit(not_a_coroutine).result()
    except Exception:
        e, tb = sys.exc_info()[1:]

        assert isinstance(e, TestException)
        assert isinstance(tb, TracebackType)

        tb_out = traceback.extract_tb(tb)
        assert "raise TestException('something went wrong')" in str(tb_out)

        return

    assert False, "should have thrown exception"


def test_use_existing_ioloop():
    io_loop = ioloop.IOLoop.current()
    threadloop = ThreadLoop(io_loop)

    assert threadloop._io_loop is io_loop

    @gen.coroutine
    def coroutine():
        raise gen.Return("Hello World")

    with threadloop:
        future = threadloop.submit(coroutine)
        assert future.result() == "Hello World"


def test_start_must_be_called_before_submit():
    threadloop = ThreadLoop()

    @gen.coroutine
    def coroutine():
        raise gen.Return("Hello World")

    with pytest.raises(ThreadNotStartedError):
        threadloop.submit(coroutine)


def test_submits_coroutines_concurrently(threadloop):

    @gen.coroutine
    def coroutine1():
        yield gen.sleep(.1)
        raise gen.Return('coroutine1')

    @gen.coroutine
    def coroutine2():
        yield gen.sleep(.1)
        raise gen.Return('coroutine2')

    @gen.coroutine
    def coroutine3():
        yield gen.sleep(.1)
        raise gen.Return('coroutine3')

    start = time.time()

    future1 = threadloop.submit(coroutine1)
    future2 = threadloop.submit(coroutine2)
    future3 = threadloop.submit(coroutine3)

    result1 = future1.result()
    result2 = future2.result()
    result3 = future3.result()

    end = time.time() - start

    # round to float with precision of 1, eg 0.3
    took = float(round(Decimal(str(end)), 1))

    # should only take ~100 ms to finish both
    # instead of ~300ms if they were executed serially
    assert took == .1

    assert result1 == 'coroutine1'
    assert result2 == 'coroutine2'
    assert result3 == 'coroutine3'


def test_as_completed(threadloop):

    @gen.coroutine
    def coroutine1():
        yield gen.sleep(.02)
        raise gen.Return('coroutine1')

    @gen.coroutine
    def coroutine2():
        yield gen.sleep(.03)
        raise gen.Return('coroutine2')

    @gen.coroutine
    def coroutine3():
        yield gen.sleep(.01)
        raise gen.Return('coroutine3')

    @gen.coroutine
    def coroutine4():
        yield gen.sleep(.04)
        raise gen.Return('coroutine4')

    futures = []
    futures.append(threadloop.submit(coroutine1))
    futures.append(threadloop.submit(coroutine2))
    futures.append(threadloop.submit(coroutine3))
    futures.append(threadloop.submit(coroutine4))

    i = 0
    for future in as_completed(futures):
        i = i + 1

        # make sure futures finish in the expected order
        if i == 1:
            assert future.result() == "coroutine3"
        elif i == 2:
            assert future.result() == "coroutine1"
        elif i == 3:
            assert future.result() == "coroutine2"
        elif i == 4:
            assert future.result() == "coroutine4"

    assert i == 4, "expected 4 completed futures"


def test_timeout(threadloop):

    @gen.coroutine
    def too_long():
        yield gen.sleep(5)  # 5 sec task
        raise gen.Return('that was too long')

    start = time.time()
    future = threadloop.submit(too_long)

    with pytest.raises(TimeoutError):
        future.result(timeout=.001)

    end = time.time() - start
    took = float(round(Decimal(str(end)), 1))

    assert took <= .002


def test_block_until_thread_is_ready():

    threadloop = ThreadLoop()

    assert not threadloop.is_ready()

    threadloop.start()

    assert threadloop.is_ready()


def test_is_not_ready_when_ready_hasnt_been_sent():

    threadloop = ThreadLoop()
    threadloop._thread = True  # fake the Thread being set

    assert not threadloop.is_ready()
