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


class DBString(ut.ExprProxy):
    """Object for storing single modifiable string.

    Manipluating STR section is hard. DBString stores only one string, so that
    modifying its structure is substantially easier than modifying entire STR
    section. You can do anything you would do with normal string with DBString.
    """

    def __init__(self, content):
        """Constructor for DBString

        :param content: Initial DBString content / capacity. Capacity of
            DBString is determined by size of this. If content is integer, then
            initial capacity and content of DBString will be set to
            content(int) and empty string.

        :type content: str, bytes, int
        """
        if isinstance(content, (int, str, bytes)):
            super().__init__(DBStringData(content))
        else:
            super().__init__(content)

    def GetStringMemoryAddr(self):
        """Get memory address of DBString content.

        :returns: Memory address of DBString content.
        """
        return self + 4

    def GetDisplayAction(self):
        """DisplayText equivilant for DBString.

        :returns: List of actions for printing DBString content.
        """
        resetter = c.Forward()
        fw = c.Forward()
        acts = [
            c.SetMemory(0x5993D4, c.SetTo, self),
            c.DisplayText(fw),
            resetter << c.SetMemory(0x5993D4, c.SetTo, 0)
        ]
        fw << ExtendedStringIndex_FW(resetter)
        return acts

    def Display(self):
        cs.DoActions(self.GetDisplayAction())


class DBStringData(c.EUDObject):
    """Object containing DBString data
    """

    def __init__(self, content):
        """Constructor for DBString

        :param content: Initial DBString content / capacity. Capacity of
            DBString is determined by size of this. If content is integer, then
            initial capacity and content of DBString will be set to
            content(int) and empty string.

        :type content: str, bytes, int
        """
        super().__init__()
        if isinstance(content, int):
            self.content = bytes(content)
        else:
            self.content = ut.u2b(content)

    def GetDataSize(self):
        return len(self.content) + 5

    def WritePayload(self, pbuf):
        pbuf.WriteBytes(b'\x01\x00\x04\x00')
        pbuf.WriteBytes(self.content)
        pbuf.WriteByte(0)


class ExtendedStringIndex_FW(c.ConstExpr):

    def __init__(self, resetter):
        super().__init__(self)
        self._resetter = resetter

    def Evaluate(self):
        _RegisterResetterAction(self._resetter)
        return c.toRlocInt(1)


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
    """Equivilant to DisplayText, but doesn't use string table to store text.

    :param text: Text to display.
    :type text: str or bytes

    .. note:: You need to call `f_initextstr` before using DisplayExtText.
    """
    text = ut.u2b(text)
    if text not in _extstr_dict:
        _extstr_dict[text] = DBString(text)
    return _extstr_dict[text].GetDisplayAction()


def _f_initextstr():
    """(internal)Initialize DBString system."""
    rb = ResetterBuffer()
    ptr, v = c.EUDVariable(), c.EUDVariable()
    ptr << ut.EPD(rb)
    origstrptr = f_dwread_epd(ut.EPD(0x5993D4))

    if cs.EUDInfLoop()():
        v << f_dwread_epd(ptr)
        cs.EUDBreakIf(v == 0xFFFFFFFF)
        f_dwwrite_epd(v, origstrptr)
        ptr += 1

    cs.EUDEndInfLoop()


def f_initextstr():
    """This function does nothing.

    .. warning::
        This function is deprecated.
    """
    pass
