from helper import *


class Coord(EUDStruct):
    _fields_ = ['x', 'y']


class Triangle(EUDStruct):
    _fields_ = [
        ('p', Coord * 5),
    ]


@TestInstance
def test_struct():
    a = Triangle()
    a.p[0].x = 1
    a.p[1].y = 2
    a.p[1].y += 2

    test_assert("Nested EUDStruct test", [
        a.p[0].x == 1,
        a.p[0].y == 0,
        a.p[1].y == 4,
    ])

    b = a.clone()
    b.p[0].x = 5
    test_equality(
        "Nested EUDStruct clone test",
        [a.p[0].x, b.p[0].x, b.p[0].y, b.p[1].y],
        [1, 5, 0, 4]
    )
