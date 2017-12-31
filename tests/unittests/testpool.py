from helper import *


# Basic struct test
class Coord(EUDStruct):
    _fields_ = ['x', 'y']


@TestInstance
def test_pool():
    pool = ObjPool(Coord)(5)

    # Basic allocation
    a = pool.alloc()
    a.x = 5
    a.y = 7

    b = pool.alloc()
    b.x = 9

    c = pool.alloc()
    c.y = 11

    test_equality(
        'Basic pool allocation',
        [a.x, a.y, b.x, c.y],
        [5, 7, 9, 11]
    )

    # freeing
    pool.free(a)
    a = None

    test_equality(
        'After freeing',
        [b.x, c.y], [9, 11]
    )

    # Reallocating some
    d = pool.alloc()
    d.x = 3
    d.y = 6
    test_equality(
        'Alloc after freeing',
        [d.x, d.y, b.x, c.y],
        [3, 6, 9, 11]
    )

    # Filling
    x = pool.alloc()
    y = pool.alloc()
    z = pool.alloc()
    w = pool.alloc()
    test_assert('Full pool', [
        x != 0, y != 0, z == 0, w == 0
    ])
