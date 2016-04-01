Changelog
=========

1.0.2 (2016-04-01)
------------------

- Fix ``concurrent.Future`` exceptions not being propagated.


1.0.1 (2015-12-17)
------------------

- Fixed a bug where instantiating ``ThreadLoop`` would change the ``IOLoop``
  for the current thread.


1.0.0 (2015-10-05)
------------------

- Commit to current API.
- Better documentation.
- Dropped support for Python 2.6.
- Dropped support for Python 3.2.


0.5.0 (2015-08-17)
------------------

- Synchronous functions (i.e., those not returning futures) can be submitted to
  the loop.


0.4.0 (2015-07-19)
------------------

- Added ``Thread.is_ready()``.
- Switched blocking mechanism to use a ``threading.Event``.


0.3.3 (2015-07-17)
------------------

- Fix race condition where submit can be called before Thread is fully started.


0.3.2 (2015-07-16)
------------------

- Fix exception traceback not propagating in python2.


0.3.1 (2015-07-13)
------------------

- Use a new IOLoop for each ThreadLoop.
