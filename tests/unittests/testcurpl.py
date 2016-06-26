from helper import *


@TestInstance
def test_curpl():
    f_setcurpl(Player2)
    a = f_getcurpl()
    f_setcurpl(Player5)
    b = f_getcurpl()
    DoActions(SetMemory(0x6509B0, SetTo, 5))
    c = f_getcurpl()
    f_setcurpl(Player1)
    test_assert("f_get/setcurpl test", [
        a == 1,
        b == 4,
        c == 5
    ])
