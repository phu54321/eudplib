from helper import *


@EUDTracedFunc
def _t1(x):
    EUDTraceLog()
    if EUDIf()(x == 0):
        EUDTraceLog()
        EUDReturn(11)
    if EUDElseIf()(x == 1):
        EUDTraceLog()
        EUDReturn(12)
    EUDEndIf()
    EUDTraceLog()
    return 13


@TestInstance
def test_trace():
    a = _t1(0)
    b = _t1(1)
    c = _t1(2)
    test_equality(
        "EUDTracedFunc works well",
        [a, b, c],
        [11, 12, 13]
    )

    for i in EUDLoopRange(10000):
        _t1(0)
        _t1(1)
        _t1(2)

    test_equality(
        "EUDTracedFunc doesn't occur stack error",
        [a, b, c],
        [11, 12, 13]
    )
