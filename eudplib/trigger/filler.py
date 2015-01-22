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

from .. import core as c
from .. import utils as ut


def dww(dstepd, v):
    act = c.Forward()
    c.SeqCompute((
        (ut.EPD(act + 16), c.SetTo, dstepd),
        (ut.EPD(act + 20), c.SetTo, v),
    ))
    c.RawTrigger(
        actions=(act << c.SetMemory(0, c.SetTo, 0))
    )


def filldw(dstepd, v1):
    c.SeqCompute((
        (dstepd, c.SetTo, v1),
    ))


@c.EUDFunc
def fillwbb(dstepd, v1, v2, v3):
    ret = c.EUDVariable()
    ret << 0

    for i in range(15, -1, -1):
        c.RawTrigger(
            conditions=v1.AtLeast(2 ** i),
            actions=[
                v1.SubtractNumber(2 ** i),
                ret.AddNumber(2 ** i)
            ]
        )

    for i in range(7, -1, -1):
        c.RawTrigger(
            conditions=v2.AtLeast(2 ** i),
            actions=[
                v2.SubtractNumber(2 ** i),
                ret.AddNumber(2 ** (i + 16))
            ]
        )

    for i in range(7, -1, -1):
        c.RawTrigger(
            conditions=v3.AtLeast(2 ** i),
            actions=[
                v3.SubtractNumber(2 ** i),
                ret.AddNumber(2 ** (i + 24))
            ]
        )

    dww(dstepd, ret)


@c.EUDFunc
def fillbbbb(dstepd, v1, v2, v3, v4):
    ret = c.EUDVariable()
    ret << 0

    vlist = (v1, v2, v3, v4)
    for i, v in enumerate(vlist):
        lsf = 8 * i
        for i in range(7, -1, -1):
            c.RawTrigger(
                conditions=v.AtLeast(2 ** i),
                actions=[
                    v.SubtractNumber(2 ** i),
                    ret.AddNumber(2 ** (i + lsf))
                ]
            )

    dww(dstepd, ret)
