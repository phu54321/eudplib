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

from . import (
    dwepdio as dwm,
    cpmemio as cpm,
    byterw as brw,
    modcurpl as cp,
)
from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

# Helper functions


@c.EUDFunc
def f_wwrite_epd(epd, subp, w):
    oldcp = cp.f_getcurpl()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(3):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * (i + 2) <= j:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([
            (c.CurrentPlayer, c.Add, k),
            (c.CurrentPlayer, c.Add, w * (256 ** i)),
        ])
        cs.EUDBreak()

    # Things gets complicated on this case.
    # We won't hand-optimize this case. This is a very, very rare case
    if cs.EUDSwitchCase()(3):
        b0, b1 = dwm.f_dwbreak(w)[2:4]
        f_bwrite_epd(epd, 3, b0)
        f_bwrite_epd(epd + 1, 0, b1)

    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)


@c.EUDFunc
def f_bwrite_epd(epd, subp, b):
    oldcp = cp.f_getcurpl()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(4):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * (i + 1) <= j:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([
            (c.EncodePlayer(c.CurrentPlayer), c.Add, k),
            (c.CurrentPlayer, c.Add, b * (256 ** i))
        ])
        cs.EUDBreak()
    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return b


# -----------------------------


@c.EUDFunc
def f_wread_epd(epd, subp):
    oldcp = cp.f_getcurpl()
    w = c.EUDVariable()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        w.SetNumber(0),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(3):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * i <= j < 8 * (i + 2):
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                        w.AddNumber(2**(j - 8 * i))
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([(c.EncodePlayer(c.CurrentPlayer), c.Add, k)])
        cs.EUDBreak()

    # Things gets complicated on this case.
    # We won't hand-optimize this case. This is a very, very rare case
    if cs.EUDSwitchCase()(3):
        dw0 = cpm.f_dwread_cp(0)
        dw1 = cpm.f_dwread_cp(1)
        w << dwm.f_dwbreak(dw0)[5] + dwm.f_dwbreak(dw1)[2] * 256

    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return w


@c.EUDFunc
def f_bread_epd(epd, subp):
    oldcp = cp.f_getcurpl()
    b = c.EUDVariable()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        b.SetNumber(0),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(4):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * i <= j < 8 * (i + 1):
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                        b.AddNumber(2**(j - 8 * i))
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([(c.EncodePlayer(c.CurrentPlayer), c.Add, k)])
        cs.EUDBreak()
    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return b
