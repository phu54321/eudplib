#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from ... import core as c
from ... import ctrlstru as cs

from . import dwmemio as dwm
from .. import calcf


_epd, _suboffset = c.EUDCreateVariables(2)


class EUDByteReader:
    def __init__(self):
        self._dw = c.EUDVariable()
        self._b = c.EUDCreateVariables(4)
        self._suboffset = c.EUDVariable()
        self._offset = c.EUDVariable()
        self._ret = c.EUDVariable()

    '''
    Seek to epd address
    '''

    def seekepd(self, epdoffset):
        c.SeqCompute([
            (self._offset, c.SetTo, epdoffset),
            (self._suboffset, c.SetTo, 0)
        ])

        c.SetVariables(self._dw, dwm.f_dwread_epd(epdoffset))

        c.SetVariables([
                           self._b[0],
                           self._b[1],
                           self._b[2],
                           self._b[3],
                       ], dwm.f_dwbreak(self._dw)[2:6])

    '''
    Seek to real address
    '''

    def seekoffset(self, offset):
        global _epd, _suboffset

        # convert offset to epd offset & suboffset
        c.SetVariables([_epd, _suboffset], calcf.f_div(offset, 4))
        c.SeqCompute([(_epd, c.Add, -0x58A364 // 4)])

        # seek to epd & set suboffset
        self.seekepd(_epd)
        c.SeqCompute([
            (self._suboffset, c.SetTo, _suboffset)
        ])

    def readbyte(self):
        case0, case1, case2, case3, swend = [c.Forward() for _ in range(5)]

        # suboffset == 0
        case0 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        c.SeqCompute([
            (self._ret, c.SetTo, self._b[0]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 1
        case1 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        c.SeqCompute([
            (self._ret, c.SetTo, self._b[1]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 2
        case2 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        c.SeqCompute([
            (self._ret, c.SetTo, self._b[2]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 3
        # read more dword
        case3 << c.NextTrigger()

        c.SeqCompute([
            (self._ret, c.SetTo, self._b[3]),
            (self._offset, c.Add, 1),
            (self._suboffset, c.SetTo, 0)
        ])

        c.SetVariables(self._dw, dwm.f_dwread_epd(self._offset))
        c.SetVariables([
                           self._b[0],
                           self._b[1],
                           self._b[2],
                           self._b[3],
                       ], dwm.f_dwbreak(self._dw)[2:6])

        swend << c.NextTrigger()
        return self._ret


class EUDByteWriter:
    def __init__(self):
        self._dw = None
        self._suboffset = None
        self._offset = None

        self._dw, self._suboffset, self._offset = c.EUDCreateVariables(3)

        self._b = [c.EUDLightVariable() for _ in range(4)]

    def seekepd(self, epdoffset):
        c.SeqCompute([
            (self._offset, c.SetTo, epdoffset),
            (self._suboffset, c.SetTo, 0)
        ])

        c.SetVariables(self._dw, dwm.f_dwread_epd(epdoffset))

        c.SetVariables([
                           self._b[0],
                           self._b[1],
                           self._b[2],
                           self._b[3],
                       ], dwm.f_dwbreak(self._dw)[2:6])

    def seekoffset(self, offset):
        global _epd, _suboffset

        # convert offset to epd offset & suboffset
        c.SetVariables([_epd, _suboffset], calcf.f_div(offset, 4))
        c.SeqCompute([(_epd, c.Add, (0x100000000 - 0x58A364) // 4)])

        self.seekepd(_epd)
        c.SeqCompute([
            (self._suboffset, c.SetTo, _suboffset)
        ])

    def writebyte(self, byte):
        case0, case1, case2, case3, swend = [c.Forward() for _ in range(5)]

        case0 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        c.SeqCompute([
            (self._b[0], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case1 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        c.SeqCompute([
            (self._b[1], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case2 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        c.SeqCompute([
            (self._b[2], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case3 << c.NextTrigger()

        c.SeqCompute([
            (self._b[3], c.SetTo, byte)
        ])

        self.flushdword()

        c.SeqCompute([
            (self._offset, c.Add, 1),
            (self._suboffset, c.SetTo, 0)
        ])

        c.SetVariables(self._dw, dwm.f_dwread_epd(self._offset))
        c.SetVariables([
                           self._b[0],
                           self._b[1],
                           self._b[2],
                           self._b[3],
                       ], dwm.f_dwbreak(self._dw)[2:6])

        swend << c.NextTrigger()

    def flushdword(self):
        # mux bytes
        c.RawTrigger(actions=self._dw.SetNumber(0))

        for i in range(7, -1, -1):
            for j in range(4):
                c.RawTrigger(
                    conditions=[
                        self._b[j].AtLeast(2 ** i)
                    ],
                    actions=[
                        self._b[j].SubtractNumber(2 ** i),
                        self._dw.AddNumber(2 ** (i + j * 8))
                    ]
                )

        dwm.f_dwwrite_epd(self._offset, self._dw)
