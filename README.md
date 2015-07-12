# ThreadLoop

[![Build Status](https://travis-ci.org/breerly/threadloop.svg?branch=master)](https://travis-ci.org/breerly/threadloop) [![Coverage Status](https://coveralls.io/repos/breerly/threadloop/badge.svg)](https://coveralls.io/r/breerly/threadloop)

> Run Tornado Coroutines from Synchronous Python.

```python

from threadloop import ThreadLoop
from tornado import gen

@gen.coroutine
def hello(greeting="Goodbye"):
    raise gen.Result("%s World" % greeting)

with ThreadLoop() as threadloop:
    future = threadloop.submit(hello, "Hello")

    print future.result() # Hello World
```
