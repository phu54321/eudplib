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
from eudplib import utils as ut


@c.EUDFunc
def f_dwepdread_epd_safe(targetplayer):
    ret, retepd = c.EUDVariable(), c.EUDVariable()

    # Common comparison rawtrigger
    c.PushTriggerScope()
    cmpc = c.Forward()
    cmp_player = cmpc + 4
    cmp_number = cmpc + 8
    cmpact = c.Forward()

    cmptrigger = c.Forward()
    cmptrigger << c.RawTrigger(
        conditions=[
            cmpc << c.Memory(0, c.AtMost, 0)
        ],
        actions=[
            cmpact << c.SetMemory(cmptrigger + 4, c.SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20
    c.PopTriggerScope()

    # static_for
    chain1 = [c.Forward() for _ in range(32)]
    chain2 = [c.Forward() for _ in range(32)]

    # Main logic start
    c.SeqCompute([
        (ut.EPD(cmp_player), c.SetTo, targetplayer),
        (ut.EPD(cmp_number), c.SetTo, 0xFFFFFFFF),
        (ret, c.SetTo, 0xFFFFFFFF),
        (retepd, c.SetTo, ut.EPD(0) + 0x3FFFFFFF)
    ])

    readend = c.Forward()

    for i in range(31, -1, -1):
        nextchain = chain1[i - 1] if i > 0 else readend
        if i >= 2:
            epdsubact = [retepd.AddNumber(-2 ** (i - 2))]
            epdaddact = [retepd.AddNumber(2 ** (i - 2))]
        else:
            epdsubact = []
            epdaddact = []

        chain1[i] << c.RawTrigger(
            nextptr=cmptrigger,
            actions=[
                c.SetMemory(cmp_number, c.Subtract, 2 ** i),
                c.SetNextPtr(cmptrigger, chain2[i]),
                c.SetMemory(cmpact_ontrueaddr, c.SetTo, nextchain),
                ret.SubtractNumber(2 ** i),
            ] + epdsubact
        )

        chain2[i] << c.RawTrigger(
            actions=[
                c.SetMemory(cmp_number, c.Add, 2 ** i),
                ret.AddNumber(2 ** i),
            ] + epdaddact
        )

    readend << c.NextTrigger()

    return ret, retepd


def f_dwread_epd_safe(targetplayer):
    return f_dwepdread_epd_safe(targetplayer)[0]


def f_epdread_epd_safe(targetplayer):
    return f_dwepdread_epd_safe(targetplayer)[1]
