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


class TestStruct(EUDStruct):
    _fields_ = ['x']

    def constructor(self, x):
        self.x = x


@EUDTypedFunc([TestStruct])
def retx(obj):
    return obj.x


@EUDTypedFunc([TestStruct, EUDFuncPtr(1, 1)])
def f1(obj, x):
    return x(obj)


@TestInstance
def test_typedfuncptr_to_funcptr():
    a = TestStruct(1)
    b = f1(a, retx)
    test_equality("Passing typedfuncptr to funcptr", b, 1)
