#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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
"""

from . import (
    dwepdio as dwm,
    cpmemio as cpm,
    byterw as brw,
    bwepdio as bwm,
    modcurpl as cp,
)
from ... import core as c, ctrlstru as cs, utils as ut

# Helper functions

_bw = brw.EUDByteWriter()
_br = brw.EUDByteReader()


def f_dwwrite(ptr, dw):
    chars = dwm.f_dwbreak(dw)[2:]
    _bw.seekoffset(ptr)
    _bw.writebyte(chars[0])
    _bw.writebyte(chars[1])
    _bw.writebyte(chars[2])
    _bw.writebyte(chars[3])


def f_wwrite(ptr, w):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    bwm.f_wwrite_epd(epd, subp, w)


def f_bwrite(ptr, b):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    bwm.f_bwrite_epd(epd, subp, b)


# -----------------------------


@c.EUDFunc
def f_dwread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    oldcp = cp.f_getcurpl()
    dw = c.EUDVariable()
    cs.DoActions([c.SetCurrentPlayer(epd), dw.SetNumber(0)])
    cs.EUDSwitch(subp)

    # Case 0
    if cs.EUDSwitchCase()(0):
        dw << cpm.f_dwread_cp(0)
        cs.EUDBreak()

    # Else → Complex
    for i in range(1, 4):
        cs.EUDSwitchCase()(i)

        for j in range(31, 8 * i - 1, -1):
            c.RawTrigger(
                conditions=c.DeathsX(c.CurrentPlayer, c.AtLeast, 1, 0, 2 ** j),
                actions=dw.AddNumber(2 ** (j - 8 * i)),
            )

        c.SeqCompute([(ut.EPD(0x6509B0), c.Add, 1)])

        for j in range(8 * i - 1, -1, -1):
            c.RawTrigger(
                conditions=c.DeathsX(c.CurrentPlayer, c.AtLeast, 1, 0, 2 ** j),
                actions=dw.AddNumber(2 ** (j + 32 - 8 * i)),
            )

        cs.EUDBreak()

    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return dw


def f_wread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    return bwm.f_wread_epd(epd, subp)


def f_bread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    return bwm.f_bread_epd(epd, subp)
