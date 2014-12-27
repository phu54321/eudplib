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

from .. import core as c
from eudplib.core import varfunc as vf

_trigtrg_runner_start = [c.Forward() for _ in range(8)]
_trigtrg_runner_end = [c.Forward() for _ in range(8)]

c.PushTriggerScope()
for player in range(8):
    _trigtrg_runner_start[player] << c.BasicTrigger(nextptr=_trigtrg_runner_end[player])
    _trigtrg_runner_end[player] << c.BasicTrigger(nextptr=~(0x51A280 + player * 12 + 4))
c.PopTriggerScope()


@vf.EUDFunc
def RunTrigTrigger():
    for player in range(8):
        nt = c.Forward()
        c.BasicTrigger(
            nextptr=_trigtrg_runner_start[player],
            actions=[
                c.SetMemory(0x6509B0, c.SetTo, player),
                c.SetNextPtr(_trigtrg_runner_end[player], nt)
            ]
        )
        nt << c.BasicTrigger(
            actions=c.SetNextPtr(_trigtrg_runner_end[player], ~(0x51A280 + player * 12 + 4))
        )
