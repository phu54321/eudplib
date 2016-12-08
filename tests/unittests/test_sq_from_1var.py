from helper import *


@TestInstance
def test_sq_from_1var():
    a, b, c, d, e = EUDCreateVariables(5)
    e << 1234
    SeqCompute([
        (a, SetTo, e),
        (b, SetTo, 1),
        (c, SetTo, 3),
        (d, SetTo, e),
        (e, SetTo, c),
        (d, SetTo, e),
    ])
    test_equality(
        "SeqCompute from 1 variable",
        [a, b, c, d, e],
        [1234, 1, 3, 3, 3]
    )


@EUDFunc
def f_shoot2(player, unittype, speed, x0, y0, x1, y1):
    test_equality(
        "f_shoot bug",
        [player, unittype, speed, x0, y0, x1, y1],
        [0, 40, 5, 768, 512, 768, 1536]
    )


@EUDFunc
def f_shoot(player, unitType, speed, tx0, ty0, tx1, ty1):
    x0 = 768 + 64 * (tx0 - 1)
    y0 = 768 + 64 * (ty0 - 1)
    x1 = 768 + 64 * (tx1 - 1)
    y1 = 768 + 64 * (ty1 - 1)
    f_shoot2(player, unitType, speed, x0, y0, x1, y1)


@EUDFunc
def f_shootU(player, unitType, speed, col):
    f_shoot(player, unitType, speed, col, -3, col, 13)


@TestInstance
def test_bwpack_seqcompute_bug():
    for i in range(100):
        f_shootU(0, 40, 5, 1)
