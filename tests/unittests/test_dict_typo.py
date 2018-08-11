from helper import *


@TestInstance
def test_dbstring_from_string():
    with expect_eperror():
        EncodeUnit("Cantina")
