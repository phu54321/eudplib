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

from eudplib import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)
from ..memiof import f_dwread_epd, f_dwwrite_epd


class DBString(c.EUDObject):

    def __init__(self, content):
        super().__init__()
        if isinstance(content, int):
            self.content = bytes(content)
        else:
            self.content = ut.u2b(content)

    def GetStringMemoryAddr(self):
        return self + 4

    def GetDataSize(self):
        return len(self.content) + 5

    def WritePayload(self, pbuf):
        pbuf.WriteBytes(b'\x01\x00\x04\x00')
        pbuf.WriteBytes(self.content)
        pbuf.WriteByte(0)

    def GetDisplayAction(self):
        resetter = c.Forward()
        fw = c.Forward()
        acts = [
            c.SetMemory(0x5993D4, c.SetTo, self),
            c.DisplayText(fw),
            resetter << c.SetMemory(0x5993D4, c.SetTo, 0)
        ]
        fw << ExtendedStringIndex_FW(resetter)
        return acts


class ExtendedStringIndex_FW(c.Expr):

    def __init__(self, resetter):
        super().__init__(self)
        self._resetter = resetter

    def Evaluate(self):
        _RegisterResetterAction(self._resetter)
        return c.RlocInt(1, 0)


_resetteracts = set()


def RCPC_ResetActionSet():
    _resetteracts.clear()


c.RegisterCreatePayloadCallback(RCPC_ResetActionSet)


def _RegisterResetterAction(resetteract):
    _resetteracts.add(resetteract)


class ResetterBuffer(c.EUDObject):

    def __init__(self):
        super().__init__()

    def GetDataSize(self):
        return (len(_resetteracts) + 1) * 4

    def WritePayload(self, pbuf):
        for ra in _resetteracts:
            pbuf.WriteDword(ut.EPD(ra + 20))
        pbuf.WriteDword(0xFFFFFFFF)


_extstr_dict = {}


def DisplayExtText(text):
    text = ut.u2b(text)
    if text not in _extstr_dict:
        _extstr_dict[text] = DBString(text)
    return _extstr_dict[text].GetDisplayAction()


def f_initextstr():
    rb = ResetterBuffer()
    ptr, v = c.EUDVariable(), c.EUDVariable()
    ptr << ut.EPD(rb)
    origstrptr = f_dwread_epd(ut.EPD(0x5993D4))

    if cs.EUDInfLoop():
        v << f_dwread_epd(ptr)
        cs.EUDBreakIf(v == 0xFFFFFFFF)
        f_dwwrite_epd(v, origstrptr)
        ptr += 1

    cs.EUDEndInfLoop()
