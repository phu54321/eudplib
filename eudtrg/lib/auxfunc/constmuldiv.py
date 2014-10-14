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


def f_constmul(number):
    if not hasattr(f_constmul, 'mulfdict'):
        f_constmul.mulfdict = {}

    mulfdict = f_constmul.mulfdict

    try:
        return mulfdict[number]
    except KeyError:
        @EUDFunc
        def mulf(a):
            ret = EUDCreateVariables(1)
            ret << 0
            for i in range(31, -1, -1):
                Trigger(
                    conditions=a.AtLeast(2**i),
                    actions=[
                        a.SubtractNumber(2**i),
                        ret.AddNumber(2**i * number)
                    ]
                )
            return ret

        mulfdict[number] = mulf
        return mulf


def f_constdiv(number):
    if not hasattr(f_constdiv, 'divfdict'):
        f_constdiv.divfdict = {}

    divfdict = f_constdiv.divfdict

    try:
        return divfdict[number]
    except KeyError:
        @EUDFunc
        def divf(a):
            ret = EUDCreateVariables(1)
            ret << 0
            for i in range(31, -1, -1):
                # number too big
                if 2**i * number >= 2**32:
                    continue

                Trigger(
                    conditions=a.AtLeast(2**i * number),
                    actions=[
                        a.SubtractNumber(2**i * number),
                        ret.AddNumber(2**i)
                    ]
                )
            return ret, a

        divfdict[number] = divf
        return divf
