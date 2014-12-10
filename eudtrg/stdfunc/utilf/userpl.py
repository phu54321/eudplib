#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..memiof import f_dwread_epd
from ... import core as c
from ... import varfunc as vf


@vf.EUDFunc
def f_getuserplayerid():
    return f_dwread_epd(c.EPD(0x512684))
