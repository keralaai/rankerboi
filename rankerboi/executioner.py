from __future__ import print_function
import sys
import threading
from time import sleep, time
try:
    import thread
except ImportError:
    import _thread as thread


_TIMED_OUT = False

def timeout_handler():
    global _TIMED_OUT
    _TIMED_OUT = True


def _timeout(s):
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, timeout_handler, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer


def execute(code, globals, timeout=None):
    if timeout is None:
        def _execute():
            try:
                exec(code, globals)
            except Exception as ex:
                globals['error'] = str(ex)
            return globals
    else:
        global _TIMED_OUT
        _TIMED_OUT = False
        @_timeout(timeout)
        def _execute():
            try:
                exec(code, globals)
            except Exception as ex:
                globals['error'] = str(ex)
            return globals

    start_time = time()
    globals = _execute()
    end_time = time()
    time_taken = end_time - start_time
    return globals, time_taken, _TIMED_OUT
