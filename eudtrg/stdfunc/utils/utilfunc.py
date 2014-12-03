#!/usr/bin/python
#-*- coding: utf-8 -*-

from ..memio import f_dwread_epd
from ... import core as c
from ... import varfunc as vf


def f_setcurpl(cp):
    cp = c.EncodePlayer(cp)
    vf.SeqCompute([
        (c.EPD(0x6509B0), c.SetTo, cp)
    ])


def f_getcurpl():
    return f_dwread_epd(c.EPD(0x6509B0))
