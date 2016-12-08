from helper import *


@TestInstance
def test_sq_from_1var():
    a, b, c = EUDCreateVariables(3)
    c << 1
    SeqCompute([
        (a, SetTo, c),
        (b, SetTo, c)
    ])
    test_equality("SeqCompute from 1 variable", [a, b, c], [1, 1, 1])
