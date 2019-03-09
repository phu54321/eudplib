#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Armoha

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
"""

from ... import core as c, ctrlstru as cs, utils as ut
from ...core.mapdata.stringmap import ForcedAddString, ApplyStringMap, GetStringMap
from ..memiof import f_getcurpl, f_setcurpl
from .cpstr import GetMapStringAddr
from .cpprint import prevcp, f_cpstr_print
from .strfunc import f_strlen_epd


class StringBuffer:
    """Object for storing single modifiable string.

    Manipluating STR section is easy. :)
    You can do anything you would do with normal string with StringBuffer.
    """

    def __init__(self, content=None):
        """Constructor for StringBuffer

        :param content: Initial StringBuffer content / capacity. Capacity of
            StringBuffer is determined by size of this. If content is integer, then
            initial capacity and content of StringBuffer will be set to
            content(int) and empty string.

        :type content: str, bytes, int
        """
        filler = ForcedAddString(b"Artani")
        if content is None:
            content = b"\r" * 1023
        elif isinstance(content, int):
            content = b"\r" * content
        else:
            content = ut.u2utf8(content)
        self.capacity = len(content)
        self.StringIndex = ForcedAddString(content)
        self.epd, self.pos = c.EUDVariable(), c.EUDVariable()
        epd = ut.EPD(GetMapStringAddr(self.StringIndex))
        c.SetVariables([self.epd, self.pos], [epd, epd])

        def _fill():
            # calculate offset of buffer string
            stroffset = []
            chkt = c.GetChkTokenized()
            strmap = GetStringMap()
            outindex = 2 * len(strmap._dataindextb) + 2

            for s in strmap._datatb:
                stroffset.append(outindex)
                outindex += len(s) + 1
            bufferoffset = stroffset[strmap._dataindextb[self.StringIndex - 1]]
            if bufferoffset % 4 != 2:
                strmap._datatb[strmap._dataindextb[filler - 1]] = b"Arta"[
                    0 : 4 - bufferoffset % 4
                ]
                strmap._capacity -= 2 + bufferoffset % 4
                ApplyStringMap(chkt)

        c.RegisterCreatePayloadCallback(_fill)

    def append(self, *args):
        prevcp << f_getcurpl()
        f_setcurpl(self.pos)
        f_cpstr_print(*args)
        self.pos << f_getcurpl()
        cs.DoActions(
            [c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0), c.SetCurrentPlayer(prevcp)]
        )

    def insert(self, index, *args):
        prevcp << f_getcurpl()
        f_setcurpl(self.epd + index)
        f_cpstr_print(*args)
        self.pos << f_getcurpl()
        f_setcurpl(prevcp)

    def delete(self, start, length=1):
        prevcp << f_getcurpl()
        index = self.epd + start
        f_setcurpl(index)
        self.pos << index
        cs.DoActions(
            [
                [
                    c.SetDeaths(c.CurrentPlayer, c.SetTo, ut.b2i4(b"\r\r\r\r"), 0),
                    c.AddCurrentPlayer(1),
                ]
                for _ in range(length)
            ]
        )
        f_setcurpl(prevcp)

    def Display(self):
        cs.DoActions(c.DisplayText(self.StringIndex))

    def Play(self):
        cs.DoActions(c.PlayWAV(self.StringIndex))

    def length(self):
        return f_strlen_epd(self.epd)
