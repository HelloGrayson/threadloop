from __future__ import absolute_import

from concurrent.futures import Future
from threading import Thread, current_thread

from tornado import ioloop

from .exceptions import ThreadNotStartedError


class ThreadLoop(object):
    """Tornado IOLoop Backed Concurrent Futures.

    Run Tornado Coroutines from Synchronous Python.

    This is made possible by starting the IOLoop in another thread. When
    coroutines are submitted, they are ran against that loop, and their
    responses are bound to Concurrent Futures.

    .. code-block:: python

        from threadloop import ThreadLoop
        from tornado import gen

        @gen.coroutine
        def coroutine(greeting="Goodbye"):
            raise gen.Result("%s World" % greeting)

        with ThreadLoop() as threadloop:

            future = threadloop.submit(coroutine, "Hello")

            print future.result() # Hello World

    """
    def __init__(self, io_loop=None):
        self.main_thread = current_thread()

        self.thread = None
        if io_loop is None:
            self.io_loop = ioloop.IOLoop()
        else:
            self.io_loop = io_loop

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        """Start IOLoop in daemonized thread."""
        assert self.thread is None, 'thread already started'
        self.thread = Thread(target=self.io_loop.start)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop IOLoop & close daemonized thread."""
        self.io_loop.stop()
        self.thread.join()

    def submit(self, fn, *args, **kwargs):
        """Submit Tornado Coroutine to IOLoop in daemonized thread.

        :param fn: Tornado Coroutine to execute
        :param args: Args to pass to coroutine
        :param kwargs: Kwargs to pass to coroutine
        :returns concurrent.futures.Future: future result of coroutine
        """
        if self.thread is None or not self.thread.isAlive():
            raise ThreadNotStartedError()

        future = Future()

        def on_done(tornado_future):
            if tornado_future.exception():
                future.set_exception(tornado_future.exception())
            else:
                future.set_result(tornado_future.result())

        self.io_loop.add_callback(
            lambda: fn(*args, **kwargs).add_done_callback(on_done)
        )

        return future
