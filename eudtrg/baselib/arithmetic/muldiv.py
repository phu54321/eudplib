from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from ..eudfunc import EUDFunc
from ..vtable import EUDVTable
from ..varassign import SetVariables, SeqCompute
from ..ctrlstru import EUDJumpIf


f_mul = f_div = None

# def for f_mul
def _f_mul_init():
    global f_mul

    vt = EUDVTable(4)
    a, b, ret, y0 = vt.GetVariables()
    f_mul_begin, f_mul_end = Forward(), Forward()
    f_mul = EUDFunc(f_mul_begin, f_mul_end, vt, 2, 1)

    PushTriggerScope()
    f_mul_begin << NextTrigger()

    # init
    SeqCompute((
        (ret, SetTo, 0),
        (y0, SetTo, b)
    ))

    """
    for i in range(31, -1, -1):
        if a > 2**i:
            a -= 2**i
            ret += 2**i * b     // 2**i * b = chain_y0[i]
    """

    chain_y0 = [Forward() for _ in range(32)]

    # Calculate chain_y0
    for i in range(32):
        SeqCompute((
            (EPD(chain_y0[i]), SetTo, y0),
            (y0, Add, y0)
        ))

    # Run multiplication chain
    for i in range(31, -1, -1):
        cy0 = Forward()

        Trigger(
            conditions = [
                a.AtLeast(2**i)
            ],
            actions = [
                a.SubtractNumber(2**i),
                cy0 << ret.AddNumber(0)
            ]
        )

        chain_y0[i] << cy0 + 20


    f_mul_end << Trigger()
    PopTriggerScope()

_f_mul_init()





def _f_div_init():
    global f_div

    vt = EUDVTable(5)
    a, b, ret, remainder, x = vt.GetVariables()
    f_div_begin, f_div_end = Forward(), Forward()
    f_div = EUDFunc(f_div_begin, f_div_end, vt, 2, 2)

    PushTriggerScope()


    # init
    f_div_begin << NextTrigger()
    SeqCompute([
        (ret, SetTo, 0),
        (x, SetTo, b),
    ])

    # chain.
    chain_x0 = [Forward() for _ in range(32)]
    chain_x1 = [Forward() for _ in range(32)]
    chain = [Forward() for _ in range(32)]

    for i in range(32):
        SeqCompute([
            (EPD(chain_x0[i]), SetTo, x),
            (EPD(chain_x1[i]), SetTo, x),
        ])

        EUDJumpIf(x.AtLeast(0x8000000), chain[i])

        SeqCompute([
            (x, Add, x),
        ])

    # Run division chain
    for i in range(31, -1, -1):
        cx0, cx1 = Forward(), Forward()
        chain[i] << Trigger(
            conditions = [
                cx0 << a.AtLeast(0)
            ],
            actions = [
                cx1 << a.SubtractNumber(0),
                ret.AddNumber(2**i)
            ]
        )

        chain_x0[i] << cx0 + 8
        chain_x1[i] << cx1 + 20

    SetVariables(remainder, a)

    f_div_end << Trigger()

    PopTriggerScope()

_f_div_init()

