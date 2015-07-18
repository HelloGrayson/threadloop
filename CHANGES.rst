Changelog
=========

0.3.3 (unreleased)
------------------

- Fix race condition where submit can be called before Thread is fully started.


0.3.2 (2015-07-16)
------------------

- Fix exception traceback not propagating in python2.


0.3.1 (2015-07-13)
------------------

- Use a new IOLoop for each ThreadLoop.
