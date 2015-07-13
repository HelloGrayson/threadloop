ThreadLoop
==========

|build-status| |coverage|

    Run Tornado Coroutines from Synchronous Python.

.. code:: python


    from threadloop import ThreadLoop
    from tornado import gen

    @gen.coroutine
    def coroutine(greeting="Goodbye"):
        raise gen.Result("%s World" % greeting)

    with ThreadLoop() as threadloop:
        future = threadloop.submit(coroutine, "Hello")

        print future.result() # Hello World


.. |build-status| image:: https://travis-ci.org/breerly/threadloop.svg?branch=0.3.1
    :target: https://travis-ci.org/breerly/threadloop

.. |coverage| image:: https://coveralls.io/repos/breerly/threadloop/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/breerly/threadloop?branch=master

