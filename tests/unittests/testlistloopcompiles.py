from helper import *


@TestInstance
def test_listloop_compiles():
    if EUDIf()(Never()):
        a, b = EUDCreateVariables(2)
        for ptr, epd in EUDLoopList(a, b):
            pass
    EUDEndIf()
