from eudtrg import LICENSE  # @UnusedImport

from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport


@EUDFunc
def f_mul(a, b):
    '''
    :returns: a * b
    '''
    ret, y0 = EUDCreateVariables(2)

    # Init
    SeqCompute([
        (ret, SetTo, 0),
        (y0, SetTo, b)
    ])

    chain = [Forward() for _ in range(32)]
    chain_y0 = [Forward() for _ in range(32)]

    # Calculate chain_y0
    for i in range(32):
        SeqCompute((
            (EPD(chain_y0[i]), SetTo, y0),
            (y0, Add, y0)
        ))
        if i <= 30:
            EUDJumpIf(a.AtMost(2 ** (i + 1) - 1), chain[i])

    # Run multiplication chain
    for i in range(31, -1, -1):
        cy0 = Forward()

        chain[i] << Trigger(
            conditions=[
                a.AtLeast(2 ** i)
            ],
            actions=[
                a.SubtractNumber(2 ** i),
                cy0 << ret.AddNumber(0)
            ]
        )

        chain_y0[i] << cy0 + 20

    return ret


@EUDFunc
def f_div(a, b):
    '''
    :returns: a//b, a % b
    '''
    ret, x = EUDCreateVariables(2)

    # Init
    SeqCompute([
        (ret, SetTo, 0),
        (x, SetTo, b),
    ])

    # Chain forward decl
    chain_x0 = [Forward() for _ in range(32)]
    chain_x1 = [Forward() for _ in range(32)]
    chain = [Forward() for _ in range(32)]

    # Fill in chain
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
            conditions=[
                cx0 << a.AtLeast(0)
            ],
            actions=[
                cx1 << a.SubtractNumber(0),
                ret.AddNumber(2 ** i)
            ]
        )

        chain_x0[i] << cx0 + 8
        chain_x1[i] << cx1 + 20

    return ret, a  # a : remainder
