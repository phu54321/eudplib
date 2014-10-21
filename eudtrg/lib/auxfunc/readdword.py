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


@bl.EUDFunc
def f_dwread_epd(targetplayer):
    '''
    Read dword from memory. This function can read any memory with read access.
    :param targetplayer: EPD Player for address to read.
    :returns: b.Memory content.
    '''
    ret = bl.EUDCreateVariables(1)

    # Common comparison trigger
    b.PushTriggerScope()
    cmp = b.Forward()
    cmp_player = cmp + 4
    cmp_number = cmp + 8
    cmpact = b.Forward()

    cmptrigger = b.Forward()
    cmptrigger << b.Trigger(
        conditions=[
            cmp << b.Memory(0, b.AtMost, 0)
        ],
        actions=[
            cmpact << b.SetMemory(cmptrigger + 4, b.SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20
    b.PopTriggerScope()

    # static_for
    chain1 = [b.Forward() for _ in range(32)]
    chain2 = [b.Forward() for _ in range(32)]

    # Main logic start
    bl.SeqCompute([
        (b.EPD(cmp_player), b.SetTo, targetplayer),
        (b.EPD(cmp_number), b.SetTo, 0xFFFFFFFF),
        (ret,             b.SetTo, 0xFFFFFFFF)
    ])

    readend = b.Forward()

    for i in range(31, -1, -1):
        nextchain = chain1[i - 1] if i > 0 else readend

        chain1[i] << b.Trigger(
            nextptr=cmptrigger,
            actions=[
                b.SetMemory(cmp_number, b.Subtract, 2 ** i),
                ret.SubtractNumber(2 ** i),
                b.SetNextPtr(cmptrigger, chain2[i]),
                b.SetMemory(cmpact_ontrueaddr, b.SetTo, nextchain)
            ]
        )

        chain2[i] << b.Trigger(
            actions=[
                b.SetMemory(cmp_number, b.Add, 2 ** i),
                ret.AddNumber(2 ** i)
            ]
        )

    readend << b.NextTrigger()

    return ret
