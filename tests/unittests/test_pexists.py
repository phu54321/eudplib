from helper import *


@TestInstance
def test_pexists():
    test_equality(
        "f_playerexist",
        [f_playerexist(0), f_playerexist(1)],
        [1, 0]
    )
