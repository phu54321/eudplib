from helper import *


# Basic struct test
class TestStruct(EUDStruct):
    _fields_ = ['x', 'y', 'z']


@TestInstance
def test_struct():
    a = TestStruct()
    a.x = 5
    a.y = 7

    b = TestStruct(a)
    c = TestStruct(b)
    d = TestStruct(c)

    b.z = 8
    c.x = 3

    test_equality(
        "EUDStruct indirect access test",
        [a.x, b.x, c.x, d.x, a.y, b.y, c.y, d.y, a.z, b.z, c.z, d.z],
        [3, 3, 3, 3, 7, 7, 7, 7, 8, 8, 8, 8]
    )


# Nested struct test

class Coord(EUDStruct):
    _fields_ = ['x', 'y']


class Triangle(EUDStruct):
    _fields_ = [
        ('p', Coord * 5),
    ]


@TestInstance
def test_nested_struct():
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
