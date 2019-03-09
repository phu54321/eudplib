import inspect
import timeit
import sys


def f():
    frame = sys._getframe(1)
    try:
        msg = "%s|%s|%s" % (
            frame.f_code.co_filename,
            frame.f_code.co_name,
            frame.f_lineno,
        )
        return msg
    finally:
        del frame


def g():
    print(f())


g()

print(timeit.timeit("f()", setup="from __main__ import f", number=1000))
