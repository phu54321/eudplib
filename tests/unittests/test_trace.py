from helper import *


@TestInstance
def test_trace():
    EUDTracePush()
    EUDTraceLog()
    EUDTraceLog()
    EUDTraceLog()
    EUDTracePop()
