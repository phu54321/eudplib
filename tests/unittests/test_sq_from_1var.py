from helper import *


@TestInstance
def test_sq_from_1var():
    a, b, c, d, e = EUDCreateVariables(5)
    e << 1234
    SeqCompute(
        [
            (a, SetTo, e),
            (b, SetTo, 1),
            (c, SetTo, 3),
            (d, SetTo, e),
            (e, SetTo, c),
            (d, SetTo, e),
        ]
    )
    test_equality("SeqCompute from 1 variable", [a, b, c, d, e], [1234, 1, 3, 3, 3])
