from helper import *


class TestStruct(EUDStruct):
    _fields_ = ['x', 'y']


@TestInstance
def test_struct():
    a = TestStruct()
    a.x = 5
    a.y = 7

    b = TestStruct(a)
    c = TestStruct(b)
    d = TestStruct(c)

    c.x = 3

    test_assert("EUDStruct test", [
        d.x == 3, d.y == 7
    ])
