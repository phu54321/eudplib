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

from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)


@c.EUDFunc
def _reader():
    ptr, epd = c.EUDVariable(), c.EUDVariable()
    ptr << 0
    epd << ut.EPD(0)
    for i in range(31, -1, -1):
        c.RawTrigger(
            conditions=[
                c.Deaths(c.CurrentPlayer, c.AtLeast, 2**i, 0)
            ],
            actions=[
                c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**i, 0),
                ptr.AddNumber(2 ** i),
                epd.AddNumber(2 ** (i - 2)) if i >= 2 else []
            ]
        )
    c.SeqCompute([(c.EncodePlayer(c.CurrentPlayer), c.SetTo, ptr)])

    return ptr, epd


def f_dwepdread_cp(cpo):
    if cpo != 0:
        cs.DoActions(c.SetMemory(0x6509B0, c.Add, cpo))
    ptr, epd = _reader()
    if cpo != 0:
        cs.DoActions(c.SetMemory(0x6509B0, c.Add, -cpo))
    return ptr, epd


def f_dwread_cp(cpo):
    return f_dwepdread_cp(cpo)[0]


def f_epdread_cp(cpo):
    return f_dwepdread_cp(cpo)[1]


def f_dwwrite_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.SetTo, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])


def f_dwadd_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.Add, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])


def f_dwsubtract_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.subtract, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])
