from __future__ import absolute_import

from threading import Thread

from concurrent.futures import Future

from tornado import ioloop


class ThreadLoop(object):
    def __init__(self, io_loop=None):
        self.thread = None
        if io_loop is None:
            self.io_loop = ioloop.IOLoop.current()
        else:
            self.io_loop = io_loop

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        assert self.thread is None, 'thread already started'
        self.thread = Thread(target=self.io_loop.start)
        self.thread.start()

    def stop(self):
        self.io_loop.stop()
        self.thread.join()

    def submit(self, fn, *args, **kwargs):
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
