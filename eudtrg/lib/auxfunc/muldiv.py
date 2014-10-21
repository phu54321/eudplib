 #!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


from eudtrg import base as b
from eudtrg.lib import baselib as bl

from .constmuldiv import f_constmul, f_constdiv


def f_mul(lhs, rhs):
    """ returns lhs*rhs """
    if isinstance(lhs, bl.EUDVariable) and isinstance(rhs, bl.EUDVariable):
        return _f_mul(lhs, rhs)

    elif isinstance(lhs, bl.EUDVariable):
        return f_constmul(rhs)(lhs)

    elif isinstance(rhs, bl.EUDVariable):
        return f_constmul(lhs)(rhs)

    else:
        return lhs * rhs


def f_div(lhs, rhs):
    """ returns (lhs//rhs, lhs%rhs) """
    if isinstance(rhs, bl.EUDVariable):
        return _f_mul(lhs, rhs)

    elif isinstance(lhs, bl.EUDVariable):
        return f_constdiv(rhs)(lhs)

    else:
        return lhs // rhs, lhs % rhs


@bl.EUDFunc
def _f_mul(lhs, rhs):
    ret, y0 = bl.EUDCreateVariables(2)

    # Init
    bl.SeqCompute([
        (ret, b.SetTo, 0),
        (y0, b.SetTo, rhs)
    ])

    chain = [b.Forward() for _ in range(32)]
    chain_y0 = [b.Forward() for _ in range(32)]

    # Calculate chain_y0
    for i in range(32):
        bl.SeqCompute((
            (b.EPD(chain_y0[i]), b.SetTo, y0),
            (y0, b.Add, y0)
        ))
        if i <= 30:
            bl.EUDJumpIf(lhs.AtMost(2 ** (i + 1) - 1), chain[i])

    # Run multiplication chain
    for i in range(31, -1, -1):
        cy0 = b.Forward()

        chain[i] << b.Trigger(
            conditions=[
                lhs.AtLeast(2 ** i)
            ],
            actions=[
                lhs.SubtractNumber(2 ** i),
                cy0 << ret.AddNumber(0)
            ]
        )

        chain_y0[i] << cy0 + 20

    return ret


@bl.EUDFunc
def _f_div(lhs, rhs):
    ret, x = bl.EUDCreateVariables(2)

    # Init
    bl.SeqCompute([
        (ret, b.SetTo, 0),
        (x, b.SetTo, rhs),
    ])

    # Chain b.forward decl
    chain_x0 = [b.Forward() for _ in range(32)]
    chain_x1 = [b.Forward() for _ in range(32)]
    chain = [b.Forward() for _ in range(32)]

    # Fill in chain
    for i in range(32):
        bl.SeqCompute([
            (b.EPD(chain_x0[i]), b.SetTo, x),
            (b.EPD(chain_x1[i]), b.SetTo, x),
        ])

        bl.EUDJumpIf(x.AtLeast(0x8000000), chain[i])

        bl.SeqCompute([
            (x, b.Add, x),
        ])

    # Run division chain
    for i in range(31, -1, -1):
        cx0, cx1 = b.Forward(), b.Forward()
        chain[i] << b.Trigger(
            conditions=[
                cx0 << lhs.AtLeast(0)
            ],
            actions=[
                cx1 << lhs.SubtractNumber(0),
                ret.AddNumber(2 ** i)
            ]
        )

        chain_x0[i] << cx0 + 8
        chain_x1[i] << cx1 + 20

    return ret, lhs  # lhs : remainder
