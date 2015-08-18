Changelog
=========

0.5.1 (unreleased)
------------------

- Nothing changed yet.


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
