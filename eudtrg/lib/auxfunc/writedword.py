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


def f_dwwrite_epd(targetplayer, value):
    '''
    Writes value to specified address.

    :param targetplayer: EPD Player of address to write value.
    :param value: Value to write.
    '''
    if isinstance(value, bl.EUDVariable):
        act = b.Forward()
        bl.SeqCompute([
            (b.EPD(act + 16), b.SetTo, targetplayer),
            (b.EPD(act + 20), b.SetTo, value)
        ])
        bl.DoActions(act << b.SetMemory(0, b.SetTo, 0))

    else:
        act = b.Forward()
        bl.SeqCompute([(b.EPD(act + 16), b.SetTo, targetplayer)])
        bl.DoActions(act << b.SetMemory(0, b.SetTo, value))
