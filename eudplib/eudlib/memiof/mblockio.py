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

from . import modcurpl as cp
from . import byterw as bm


@c.EUDFunc
def f_repmovsd_epd(dstepdp, srcepdp, copydwn):
    epd_diff = dstepdp - srcepdp
    tempv = c.Forward()

    # Backup original cp.
    origcp = cp.f_getcurpl()

    cp.f_setcurpl(srcepdp)

    # Set cpmodas.
    cpmoda1_list = [c.Forward() for _ in range(32)]
    cpmoda2_list = [c.Forward() for _ in range(32)]
    cpmoda0_list = [c.Forward(), c.Forward()]
    cs.DoActions([
        [c.SetMemory(cpmoda1 + 20, c.SetTo, epd_diff)
            for cpmoda1 in cpmoda1_list],
        [c.SetMemory(cpmoda2 + 20, c.SetTo, -epd_diff)
            for cpmoda2 in cpmoda2_list],
        [
            c.SetMemory(cpmoda0_list[0] + 20, c.SetTo, epd_diff),
            c.SetMemory(cpmoda0_list[1] + 20, c.SetTo, -epd_diff),
        ]
    ])

    if cs.EUDWhileNot()(copydwn == 0):
        cpmoda01, cpmoda02 = cpmoda0_list

        # *dstepdp, tempv = 0
        c.RawTrigger(
            actions=[
                cpmoda01 << c.SetMemory(0x6509B0, c.Add, 0),
                c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0),
                cpmoda02 << c.SetMemory(0x6509B0, c.Add, 0),
                c.SetMemory(tempv, c.SetTo, 0),
            ]
        )

        for i in range(31, -1, -1):
            cpmoda1, cpmoda2 = cpmoda1_list[i], cpmoda2_list[i]
            # if *srcepdp >= 2**i:
            #     *srcepdp -= 2 ** i
            #     *dstepdp += 2 ** i
            #     tempv += 2 ** i
            c.RawTrigger(
                conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2 ** i, 0),
                actions=[
                    c.SetDeaths(c.CurrentPlayer, c.Subtract, 2 ** i, 0),
                    cpmoda1 << c.SetMemory(0x6509B0, c.Add, 0),
                    c.SetDeaths(c.CurrentPlayer, c.Add, 2 ** i, 0),
                    cpmoda2 << c.SetMemory(0x6509B0, c.Add, 0),
                    c.SetMemory(tempv, c.Add, 2 ** i),
                ]
            )

        resetteract = c.Forward()
        tempv << resetteract + 20

        c.RawTrigger(
            actions=[
                resetteract << c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0),
                c.SetMemory(0x6509B0, c.Add, 1),
                copydwn.SubtractNumber(1),
            ]
        )

    cs.EUDEndWhile()

    cp.f_setcurpl(origcp)


# -------


_br = bm.EUDByteReader()
_bw = bm.EUDByteWriter()


@c.EUDFunc
def f_memcpy(dst, src, copylen):
    b = c.EUDVariable()

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = c.NextTrigger()
    loopend = c.Forward()

    cs.EUDJumpIf(copylen.Exactly(0), loopend)

    c.SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    cs.DoActions(copylen.SubtractNumber(1))
    cs.EUDJump(loopstart)

    loopend << c.NextTrigger()


@c.EUDFunc
def f_memcmp(buf1, buf2, count):
    _br.seekoffset(buf1)
    _bw.seekoffset(buf2)

    if cs.EUDWhile()(count >= 1):
        count -= 1
        ch1 = _br.readbyte()
        ch2 = _bw.readbyte()
        cs.EUDContinueIf(ch1 == ch2)
        c.EUDReturn(ch1 - ch2)
    cs.EUDEndWhile()

    c.EUDReturn(0)
