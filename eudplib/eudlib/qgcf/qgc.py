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
    utils as ut
)

from ..memiof import f_dwread_epd, f_memcpy


@c.EUDFunc
def QueueGameCommand(buf, size):
    prov_maxbuffer = f_dwread_epd(ut.EPD(0x57F0D8))
    cmdqlen = f_dwread_epd(ut.EPD(0x654AA0))
    if cs.EUDIfNot(cmdqlen + size + 1 >= prov_maxbuffer):
        f_memcpy(0x654880 + cmdqlen, buf, size)
        c.SetVariables(ut.EPD(0x654AA0), cmdqlen + size)
    cs.EUDEndIf()


@c.EUDFunc
def QueueGameCommand_RightClick(x):
    RightClickCommand = c.Db(b'...\x14XXYY\0\0\xE4\0\x00')
    c.SetVariables(ut.EPD(RightClickCommand + 4), x)
    QueueGameCommand(RightClickCommand + 3, 10)
