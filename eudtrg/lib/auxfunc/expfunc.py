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

from .muldiv import f_mul, f_div


@bl.EUDFunc
def f_exp(lhs, rhs):
    global f_exp

    ret = bl.EUDCreateVariables(1)

    expvar = bl.EUDCreateVariables(32)

    chain = [b.Forward() for _ in range(32)]
    ret << 1
    expvar[0] << lhs

    for i in range(1, 31):
        bl.EUDJumpIf(expvar[i - 1].Exactly(0), chain[i - 1])
        bl.EUDJumpIf(rhs.AtMost(2 ** i - 1), chain[i - 1])

        bl.SetVariables(expvar[i], f_mul(expvar[i - 1], expvar[i - 1]))

        skipcond_skip = b.Forward()
        bl.EUDJumpIfNot(expvar[i].Exactly(1), skipcond_skip)

        bl.SetVariables(rhs, f_div(rhs, 2 ** i)[1])
        bl.EUDJump(chain[i - 1])

        skipcond_skip << b.NextTrigger()

    for i in range(31, -1, -1):
        chain[i] << b.NextTrigger()

        mul_skip = b.Forward()
        bl.EUDJumpIfNot(rhs.AtLeast(2 ** i), mul_skip)

        bl.SeqCompute((
            (rhs, b.Subtract, 2 ** i),
            (ret, b.SetTo, f_mul(ret, expvar[i]))
        ))

        mul_skip << b.NextTrigger()

    return ret
