#!/usr/bin/python
# -*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf

from . import byterw as bm


_br = bm.EUDByteReader()
_bw = bm.EUDByteWriter()


@vf.EUDFunc
def f_strcpy(dst, src):
    '''
    strcpy equivilant in eudtrg. Copy C-style string.

    :param dst: Destination address. (Not EPD Player)
    :param src: Source address. (Not EPD Player)
    '''
    b = vf.EUDVariable()

    _br.seekoffset(src)
    _bw.seekoffset(dst)

    loopstart = c.NextTrigger()

    vf.SetVariables(b, _br.readbyte())
    _bw.writebyte(b)

    cs.EUDJumpIfNot(b.Exactly(0), loopstart)

    _bw.flushdword()
