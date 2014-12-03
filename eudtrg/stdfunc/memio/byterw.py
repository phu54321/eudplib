#!/usr/bin/python
#-*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf

from . import dwmemio as dwm
from .. import math


_epd, _suboffset = vf.EUDCreateVariables(2)


class EUDByteReader:

    def __init__(self):
        self._dw = vf.EUDVariable()
        self._b = vf.EUDCreateVariables(4)
        self._suboffset = vf.EUDVariable()
        self._offset = vf.EUDVariable()
        self._ret = vf.EUDVariable()

    '''
    Seek to epd address
    '''

    def seekepd(self, epdoffset):
        vf.SeqCompute([
            (self._offset, c.SetTo, epdoffset),
            (self._suboffset, c.SetTo, 0)
        ])

        vf.SetVariables(self._dw, dwm.f_dwread_epd(epdoffset))

        vf.SetVariables([
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
        vf.SetVariables([_epd, _suboffset], math.f_div(offset, 4))
        vf.SeqCompute([(_epd, c.Add, -0x58A364 // 4)])

        # seek to epd & set suboffset
        self.seekepd(_epd)
        vf.SeqCompute([
            (self._suboffset, c.SetTo, _suboffset)
        ])

    def readbyte(self):
        case0, case1, case2, case3, swend = [c.Forward() for _ in range(5)]

        # suboffset == 0
        case0 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        vf.SeqCompute([
            (self._ret, c.SetTo, self._b[0]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 1
        case1 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        vf.SeqCompute([
            (self._ret, c.SetTo, self._b[1]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 2
        case2 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        vf.SeqCompute([
            (self._ret, c.SetTo, self._b[2]),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        # suboffset == 3
        # read more dword
        case3 << c.NextTrigger()

        vf.SeqCompute([
            (self._ret, c.SetTo, self._b[3]),
            (self._offset, c.Add, 1),
            (self._suboffset, c.SetTo, 0)
        ])

        vf.SetVariables(self._dw, dwm.f_dwread_epd(self._offset))
        vf.SetVariables([
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

        self._dw, self._suboffset, self._offset = vf.EUDCreateVariables(3)

        self._b = [vf.EUDLightVariable() for _ in range(4)]

    def seekepd(self, epdoffset):
        vf.SeqCompute([
            (self._offset, c.SetTo, epdoffset),
            (self._suboffset, c.SetTo, 0)
        ])

        vf.SetVariables(self._dw, dwm.f_dwread_epd(epdoffset))

        vf.SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], dwm.f_dwbreak(self._dw)[2:6])

    def seekoffset(self, offset):
        global _epd, _suboffset

        # convert offset to epd offset & suboffset
        vf.SetVariables([_epd, _suboffset], math.f_div(offset, 4))
        vf.SeqCompute([(_epd, c.Add, (0x100000000 - 0x58A364) // 4)])

        self.seekepd(_epd)
        vf.SeqCompute([
            (self._suboffset, c.SetTo, _suboffset)
        ])

    def writebyte(self, byte):
        case0, case1, case2, case3, swend = [c.Forward() for _ in range(5)]

        case0 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        vf.SeqCompute([
            (self._b[0], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case1 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(1), case2)
        vf.SeqCompute([
            (self._b[1], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case2 << c.NextTrigger()
        cs.EUDJumpIfNot(self._suboffset.Exactly(2), case3)
        vf.SeqCompute([
            (self._b[2], c.SetTo, byte),
            (self._suboffset, c.Add, 1)
        ])
        cs.EUDJump(swend)

        case3 << c.NextTrigger()

        vf.SeqCompute([
            (self._b[3], c.SetTo, byte)
        ])

        self.flushdword()

        vf.SeqCompute([
            (self._offset, c.Add, 1),
            (self._suboffset, c.SetTo, 0)
        ])

        vf.SetVariables(self._dw, dwm.f_dwread_epd(self._offset))
        vf.SetVariables([
            self._b[0],
            self._b[1],
            self._b[2],
            self._b[3],
        ], dwm.f_dwbreak(self._dw)[2:6])

        swend << c.NextTrigger()

    def flushdword(self):
        # mux bytes
        c.Trigger(actions=self._dw.SetNumber(0))

        for i in range(7, -1, -1):
            for j in range(4):
                c.Trigger(
                    conditions=[
                        self._b[j].AtLeast(2 ** i)
                    ],
                    actions=[
                        self._b[j].SubtractNumber(2 ** i),
                        self._dw.AddNumber(2 ** (i + j * 8))
                    ]
                )

        dwm.f_dwwrite_epd(self._offset, self._dw)
