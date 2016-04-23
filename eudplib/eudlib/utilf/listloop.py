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

from ..memiof import f_dwepdread_epd
from eudplib import (
    core as c,
    ctrlstru as cs,
    utils as ut,
    trigtrg as tt
)


def EUDLoopList(header_offset, break_offset=None):
    blockname = 'listloop'
    ut.EUDCreateBlock(blockname, header_offset)

    ptr, epd = f_dwepdread_epd(ut.EPD(header_offset))

    if break_offset is not None:
        cs.EUDWhileNot()(ptr == break_offset)
    else:
        cs.EUDWhile()([ptr >= 0, ptr <= 0x7FFFFFFF])

    yield ptr, epd
    cs.EUDSetContinuePoint()
    c.SetVariables([ptr, epd], f_dwepdread_epd(epd + 1))
    cs.EUDEndWhile()

    ut.ep_assert(
        ut.EUDPopBlock(blockname)[1] == header_offset,
        'listloop mismatch'
    )


def EUDLoopUnit():
    for ptr, epd in EUDLoopList(0x628430):
        yield ptr, epd


def EUDLoopBullet():
    for ptr, epd in EUDLoopList(0x64DEC4):
        yield ptr, epd


def EUDLoopSprite():
    y_epd = c.EUDVariable()
    y_epd << ut.EPD(0x629688)

    ut.EUDCreateBlock('listloop', 'sprlo')

    if cs.EUDWhile()(y_epd < ut.EPD(0x629688) + 256):
        ptr, epd = f_dwepdread_epd(y_epd)
        if cs.EUDWhile()(ptr >= 1):
            yield ptr, epd
            cs.EUDSetContinuePoint()
            c.SetVariables([ptr, epd], f_dwepdread_epd(epd + 1))
        cs.EUDEndWhile()
        y_epd += 1
    cs.EUDEndWhile()

    ut.EUDPopBlock('spriteloop')


def EUDLoopTrigger(player):
    player = c.EncodePlayer(player)

    cs.DoActions([
        c.SetMemoryEPD(0, c.SetTo, tt.TrigTriggerBegin(player)),
        c.SetMemoryEPD(1, c.SetTo, tt.GetLastTrigTrigger(player)),
    ])

    for ptr, epd in EUDLoopList(
        tt.TrigTriggerBegin(player),
        tt.TrigTriggerEnd(player)
    ):
        yield ptr, epd
