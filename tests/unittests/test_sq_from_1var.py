from helper import *


@TestInstance
def test_sq_from_1var():
    a, b, c, d, e = EUDCreateVariables(5)
    e << 1234
    SeqCompute([
        (a, SetTo, e),
        (b, SetTo, e),
        (c, SetTo, e),
        (d, SetTo, e),
        (e, SetTo, e),
    ])
    test_equality(
        "SeqCompute from 1 variable",
        [a, b, c, d, e],
        [1234, 1234, 1234, 1234, 1234]
    )
