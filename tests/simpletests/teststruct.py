from helper import *


class TestStruct(EUDStruct):
    _fields_ = ['x', 'y']


@TestInstance
def test_struct():
    a = TestStruct()
    a.x = 5
    a.y = 7

    b = TestStruct(a.addr())
    c = TestStruct(b.addr())
    d = TestStruct(c.addr())

    c.x = 3

    test_assert("EUDStruct test", [
        d.x == 3, d.y == 7
    ])
