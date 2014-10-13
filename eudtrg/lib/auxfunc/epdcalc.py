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

from .muldiv import f_div


@EUDFunc
def f_epd(addr):
    '''
    Convert address to EPD Player value. Use :func:`EPD` instead to convert
    Expr to EPD player value.

    :param addr: Address to convert.
    :returns: EPD player corresponding to given address.

    '''
    epd = EUDCreateVariables(1)
    DoActions(addr.AddNumber(-0x58A364))
    SetVariables(epd, f_div(addr, 4)[0])
    return epd
