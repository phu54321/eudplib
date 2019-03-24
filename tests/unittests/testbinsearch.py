from helper import *


@TestInstance
def test_binsearch():
    n = EUDVariable()

    # Basic test
    n << 1000
    p1 = EUDBinaryMin(lambda x: x * x >= n, 0, 0xFFFF)
    p2 = EUDBinaryMax(lambda x: x * x <= n, 0, 0xFFFF)
    test_equality("Binary search - Square root test", [p1, p2], [32, 31])

    # Specific range test
    @EUDFunc
    def comp1(x):
        if EUDIf()(x <= 30):
            EUDReturn(0)
        if EUDElseIf()(x >= 70):
            EUDReturn(0)
        if EUDElseIf()(x <= 40):
            EUDReturn(1)
        if EUDElse()():
            EUDReturn(0)
        EUDEndIf()

    p3 = EUDBinaryMax(comp1, 31, 69)

    @EUDFunc
    def comp1(x):
        if EUDIf()(x <= 30):
            EUDReturn(0)
        if EUDElseIf()(x >= 70):
            EUDReturn(0)
        if EUDElseIf()(x >= 40):
            EUDReturn(1)
        if EUDElse()():
            EUDReturn(0)
        EUDEndIf()

    p4 = EUDBinaryMin(comp1, 31, 69)

    test_equality("Binary search - bounded range test", [p3, p4], [40, 40])
