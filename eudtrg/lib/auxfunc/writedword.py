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


def f_dwwrite(targetplayer, value):
    '''
    Writes value to specified address.

    :param targetplayer: EPD Player of address to write value.
    :param value: Value to write.
    '''
    if isinstance(value, EUDVariable):
        act = Forward()
        SeqCompute([
            (EPD(act + 16), SetTo, targetplayer),
            (EPD(act + 20), SetTo, value)
        ])
        DoActions(act << SetMemory(0, SetTo, 0))

    else:
        act = Forward()
        SeqCompute([(EPD(act + 16), SetTo, targetplayer)])
        DoActions(act << SetMemory(0, SetTo, value))
