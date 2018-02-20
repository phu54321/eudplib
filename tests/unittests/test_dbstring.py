from helper import *


@TestInstance
def test_dbstring_from_string():
    a = DBString.cast("test")
    a.Display()
