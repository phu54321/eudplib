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
from eudplib.core import varfunc as vf

from . import dwmemio as dwm
from . import byterw as bm


@vf.EUDFunc
def f_repmovsd_epd(dstepdp, srcepdp, copydwn):
    repmovsd_end = c.Forward()

    loopstart = c.NextTrigger()
    cs.EUDJumpIf(copydwn.Exactly(0), repmovsd_end)

    dwm.f_dwwrite_epd(dstepdp, dwm.f_dwread_epd(srcepdp))
    vf.SeqCompute([
        (srcepdp, c.Add, 1),
        (dstepdp, c.Add, 1),
        (copydwn, c.Subtract, 1)
    ])

    cs.EUDJump(loopstart)

    repmovsd_end << c.NextTrigger()


# -------


_br = bm.EUDByteReader()
_bw = bm.EUDByteWriter()


@vf.EUDFunc
def f_memcpy(dst, src, copylen):
    b = vf.EUDVariable()

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = c.NextTrigger()
    loopend = c.Forward()

    cs.EUDJumpIf(copylen.Exactly(0), loopend)

    vf.SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    cs.DoActions(copylen.SubtractNumber(1))
    cs.EUDJump(loopstart)

    loopend << c.NextTrigger()
    _bw.flushdword()
