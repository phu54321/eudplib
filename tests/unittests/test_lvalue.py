from helper import *


@TestInstance
def test_operator_lvalue():
    a, b = EUDVariable(), EUDVariable()
    with expect_eperror():
        (a + b) << 5

    with expect_eperror():
        (a * b) << 5


@TestInstance
def test_function_lvalue():
    with expect_eperror():
        a = f_dwread_epd(0)
        a << 5
