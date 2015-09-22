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

from ..memiof import f_dwread_epd
from .modcurpl import (
    f_getcurpl,
    f_setcurpl,
)

from eudplib import (
    core as c,
    ctrlstru as cs,
    utils as ut
)


@c.EUDFunc
def f_playerexist(player):
    pts = 0x51A280

    ret = c.EUDVariable()
    prevtstart = f_dwread_epd(ut.EPD(pts + player * 12 + 8))
    if cs.EUDIf(prevtstart == ~(pts + player * 12 + 4)):
        ret << 0
    if cs.EUDElse():
        ret << 1
    cs.EUDEndIf()
    return ret


# --------

def EUDPlayerLoop():
    block = {'origcp': f_getcurpl(), 'playerv': c.EUDVariable()}
    playerv = block['playerv']

    playerv << 0
    cs.EUDWhile(playerv <= 7)
    cs.EUDContinueIfNot(f_playerexist(playerv))
    f_setcurpl(playerv)

    ut.EUDCreateBlock('ploopblock', block)
    return True


def EUDEndPlayerLoop():
    block = ut.EUDPopBlock('ploopblock')[1]
    playerv = block['playerv']
    origcp = block['origcp']

    if not cs.EUDIsContinuePointSet():
        cs.EUDSetContinuePoint()

    playerv += 1
    cs.EUDEndWhile()
    f_setcurpl(origcp)
