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


@EUDFunc
def f_dwbreak(number):
    '''
    Break dword into words & dwords.

    :param number: Number to break.
    :returns: w[0], w[1], b[0], b[1], b[2], b[3] ::

        union {
            DWORD number;
            WORD w[2];
            BYTE b[4];
        }
    '''
    word = [None] * 2
    byte = [None] * 4
    (word[0], word[1], byte[0], byte[1],
        byte[2], byte[3]) = EUDCreateVariables(6)

    # Clear byte[], word[]
    DoActions([
        word[0].SetNumber(0),
        word[1].SetNumber(0),
        byte[0].SetNumber(0),
        byte[1].SetNumber(0),
        byte[2].SetNumber(0),
        byte[3].SetNumber(0)
    ])

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16
        byteexp = i % 8
        wordexp = i % 16

        Trigger(
            conditions=number.AtLeast(2**i),
            actions=[
                byte[byteidx].AddNumber(2**byteexp),
                word[wordidx].AddNumber(2**wordexp),
                number.SubtractNumber(2**i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]
