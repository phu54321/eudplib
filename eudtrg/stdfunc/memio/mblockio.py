#!/usr/bin/python
#-*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf

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
