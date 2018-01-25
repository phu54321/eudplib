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
)


def f_setcurpl(cp):
    cs.DoActions(c.SetCurrentPlayer(cp))


# This function initializes _curpl_checkcond, so should be called at least once
@c.EUDFunc
def _f_updatecpcache():
    cpcache = c.curpl.GetCPCache()
    cpcache << 0
    for i in range(31, -1, -1):
        c.RawTrigger(
            conditions=[c.Memory(0x6509B0, c.AtLeast, 2**i)],
            actions=[
                c.SetMemory(0x6509B0, c.Subtract, 2**i),
                cpcache.AddNumber(2**i)
            ]
        )
    cs.DoActions(c.SetCurrentPlayer(cpcache))


@c.EUDFunc
def f_getcurpl():
    """Get current player value.

    eudplib internally caches the current player value, so this function uses
    that value if the value is valid. Otherwise, update the current player
    cache and return it.
    """
    cpcond = c.curpl.cpcacheMatchCond()
    cpcache = c.curpl.GetCPCache()
    if cs.EUDIfNot()(cpcond):
        _f_updatecpcache()
    cs.EUDEndIf()

    return cpcache
