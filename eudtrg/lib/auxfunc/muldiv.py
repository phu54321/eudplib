'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''

from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport

from .constmuldiv import f_constmul, f_constdiv


def f_mul(a, b):
    if isinstance(a, EUDVariable) and isinstance(b, EUDVariable):
        return _f_mul(a, b)

    elif isinstance(a, EUDVariable):
        return f_constmul(b)(a)

    elif isinstance(b, EUDVariable):
        return f_constmul(a)(b)

    else:
        return a*b


def f_div(a, b):
    if isinstance(b, EUDVariable):
        return _f_mul(a, b)

    elif isinstance(a, EUDVariable):
        return f_constdiv(b)(a)

    else:
        return a // b, a % b


@EUDFunc
def _f_mul(a, b):
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
def _f_div(a, b):
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
