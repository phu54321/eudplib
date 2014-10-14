from eudtrg.base import *
from eudtrg.lib.baselib import *
from .muldiv import f_mul, f_div


@EUDFunc
def f_exp(a, b):
    global f_exp

    ret = EUDCreateVariables(1)

    expvt = EUDVTable(32)
    expvar = expvt.GetVariables()

    chain = [Forward() for _ in range(32)]
    ret << 1
    expvar[0] << a

    for i in range(1, 31):
        EUDJumpIf(expvar[i - 1].Exactly(0), chain[i - 1])
        EUDJumpIf(b.AtMost(2**i - 1), chain[i - 1])

        SetVariables(expvar[i], f_mul(expvar[i - 1], expvar[i - 1]))

        skipcond_skip = Forward()
        EUDJumpIfNot(expvar[i].Exactly(1), skipcond_skip)

        SetVariables(b, f_div(b, 2**i)[1])
        EUDJump(chain[i - 1])

        skipcond_skip << NextTrigger()

    for i in range(31, -1, -1):
        chain[i] << NextTrigger()

        mul_skip = Forward()
        EUDJumpIfNot(b.AtLeast(2**i), mul_skip)

        SeqCompute((
            (b, Subtract, 2**i),
            (ret, SetTo, f_mul(ret, expvar[i]))
        ))

        mul_skip << NextTrigger()

    return ret
