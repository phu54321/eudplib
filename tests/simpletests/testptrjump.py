from helper import *


@TestInstance
def test_ptrjump():
    testvar = EUDVariable()
    a = EUDVariable()
    t = Forward()

    testvar += 1
    a << t
    testvar += 2
    EUDJump(t)
    testvar += 4
    t << NextTrigger()
    testvar += 8

    test_assert("test_ptrjump", testvar == 11)
