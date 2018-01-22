from helper import *


@TestInstance
def test_trace():
    EUDTracePush()
    EUDTraceLog(1)
    EUDTraceLog(2)
    EUDTracePop()
