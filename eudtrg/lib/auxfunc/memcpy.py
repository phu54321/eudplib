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

from eudtrg.base import *
from eudtrg.lib.baselib import *

from .readdword import f_dwread_epd
from .writedword import f_dwwrite_epd
from .dwordbreak import f_dwbreak
from .muldiv import f_div


# Faster function
@EUDFunc
def f_repmovsd(dstepdp, srcepdp, copydwn):
    '''
    rep movsd equivilant in eudtrg. Copy dwords. Faster than f_memcpy.

    :param dstepdp: EPD Player for destination.
    :param srcepdp: EPD Player for source.
    :param copydwn: Count of dwords to copy.
    '''
    repmovsd_end = Forward()

    loopstart = NextTrigger()
    EUDJumpIf(copydwn.Exactly(0), repmovsd_end)

    f_dwwrite_epd(dstepdp, f_dwread_epd(srcepdp))
    SeqCompute([
        (srcepdp, Add, 1),
        (dstepdp, Add, 1),
        (copydwn, Subtract, 1)
    ])

    EUDJump(loopstart)

    repmovsd_end << NextTrigger()


_epd, _suboffset = EUDCreateVariables(2)

# String copy


class EUDByteReader:

    def __init__(self):
        self._dw = None
        self._b = [None] * 4
        self._suboffset = None
        self._offset = None
        self._ret = None

        self._dw, self._b[0], self._b[1], self._b[2], self._b[3], \
            self._suboffset, self._offset, self._ret = EUDCreateVariables(8)

    '''
    Seek to epd address
    '''

    def seekepd(self, epdoffset):
        SeqCompute([
            (self._offset, SetTo, epdoffset),
            (self._suboffset, SetTo, 0)
        ])

        SetVariables(self._dw, f_dwread_epd(epdoffset))

        SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], f_dwbreak(self._dw)[2:6])

    '''
    Seek to real address
    '''

    def seekoffset(self, offset):
        global _epd, _suboffset

        # convert offset to epd offset & suboffset
        SetVariables([_epd, _suboffset], f_div(offset, 4))
        SeqCompute([(_epd, Add, (0x100000000 - 0x58A364) // 4)])

        # seek to epd & set suboffset
        self.seekepd(_epd)
        SeqCompute([
            (self._suboffset, SetTo, _suboffset)
        ])

    def readbyte(self):
        case0, case1, case2, case3, swend = Forward(
        ), Forward(), Forward(), Forward(), Forward()

        # suboffset == 0
        case0 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        SeqCompute([
            (self._ret, SetTo, self._b[0]),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        # suboffset == 1
        case1 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        SeqCompute([
            (self._ret, SetTo, self._b[1]),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        # suboffset == 2
        case2 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        SeqCompute([
            (self._ret, SetTo, self._b[2]),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        # suboffset == 3
        # read more dword
        case3 << NextTrigger()

        SeqCompute([
            (self._ret, SetTo, self._b[3]),
            (self._offset, Add, 1),
            (self._suboffset, SetTo, 0)
        ])

        SetVariables(self._dw, f_dwread_epd(self._offset))
        SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], f_dwbreak(self._dw)[2:6])

        swend << NextTrigger()
        return self._ret


class EUDByteWriter:

    def __init__(self):
        self._dw = None
        self._suboffset = None
        self._offset = None

        self._dw, self._suboffset, self._offset = EUDCreateVariables(3)

        self._b = [EUDLightVariable() for _ in range(4)]

    def seekepd(self, epdoffset):
        SeqCompute([
            (self._offset, SetTo, epdoffset),
            (self._suboffset, SetTo, 0)
        ])

        SetVariables(self._dw, f_dwread_epd(epdoffset))

        SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], f_dwbreak(self._dw)[2:6])

    def seekoffset(self, offset):
        global _epd, _suboffset

        # convert offset to epd offset & suboffset
        SetVariables([_epd, _suboffset], f_div(offset, 4))
        SeqCompute([(_epd, Add, (0x100000000 - 0x58A364) // 4)])

        self.seekepd(_epd)
        SeqCompute([
            (self._suboffset, SetTo, _suboffset)
        ])

    def writebyte(self, byte):
        case0, case1, case2, case3, swend = Forward(
        ), Forward(), Forward(), Forward(), Forward()

        case0 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        SeqCompute([
            (self._b[0], SetTo, byte),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        case1 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        SeqCompute([
            (self._b[1], SetTo, byte),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        case2 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        SeqCompute([
            (self._b[2], SetTo, byte),
            (self._suboffset, Add, 1)
        ])
        EUDJump(swend)

        case3 << NextTrigger()

        SeqCompute([
            (self._b[3], SetTo, byte)
        ])

        self.flushdword()

        SeqCompute([
            (self._offset, Add, 1),
            (self._suboffset, SetTo, 0)
        ])

        SetVariables(self._dw, f_dwread_epd(self._offset))
        SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], f_dwbreak(self._dw)[2:6])

        swend << NextTrigger()

    def flushdword(self):
        # mux bytes
        DoActions(self._dw.SetNumber(0))

        for i in range(7, -1, -1):
            for j in range(4):
                Trigger(
                    conditions=[
                        self._b[j].AtLeast(2 ** i)
                    ],
                    actions=[
                        self._b[j].SubtractNumber(2 ** i),
                        self._dw.AddNumber(2 ** (i + j * 8))
                    ]
                )

        f_dwwrite_epd(self._offset, self._dw)

_br = EUDByteReader()
_bw = EUDByteWriter()


@EUDFunc
def f_memcpy(dst, src, copylen):
    '''
    memcpy equivilant in eudtrg. Copy bytes.

    :param dst: Destination address. (Not EPD Player)
    :param src: Source address. (Not EPD Player)
    :param copylen: Count of bytes to copy.
    '''
    b = EUDCreateVariables(1)

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = NextTrigger()
    loopend = Forward()

    EUDJumpIf(copylen.Exactly(0), loopend)

    SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    DoActions(copylen.SubtractNumber(1))
    EUDJump(loopstart)

    loopend << NextTrigger()
    _bw.flushdword()


@EUDFunc
def f_strcpy(dst, src):
    '''
    strcpy equivilant in eudtrg. Copy C-style string.

    :param dst: Destination address. (Not EPD Player)
    :param src: Source address. (Not EPD Player)
    '''
    b = EUDCreateVariables(1)

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = NextTrigger()

    SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    EUDJumpIfNot(b.Exactly(0), loopstart)

    _bw.flushdword()
