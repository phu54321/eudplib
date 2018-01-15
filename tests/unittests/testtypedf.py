from helper import *


@EUDFunc
def f_mul(a, b):
    return a * b


@EUDFunc
def f_add(a, b):
    return a + b


@EUDFunc
def f_addmul(a, b):
    return a + b, a * b


@EUDTypedFunc([EUDFuncPtr(2, 1), None, None], [None])
def indirectcaller(f, a, b):
    return f(a, b)


@TestInstance
def test_typedfunc():
    a = indirectcaller(f_mul, 3, 6)
    test_equality("Simple indirect call", [a], [18])

    tptr = EUDTypedFuncPtr(
        [EUDFuncPtr(2, 1), None, None], [None]
    )(indirectcaller)
    b = tptr(f_add, 3, 6)
    test_equality("Typed function call via function pointer", [b], [9])
