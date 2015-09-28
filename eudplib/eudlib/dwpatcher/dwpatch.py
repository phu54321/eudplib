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

from ... import stdobj as so
from ... import core as c
from ... import ctrlstru as cs
from ..memiof import f_dwread_epd, f_dwwrite_epd

patcharr = so.EUDArray(16384)  # 64kb of buffer
patchsize = c.EUDVariable()

@c.EUDFunc
def f_dwpatch(addrepd, value):
    global patchsize
    origvalue = f_dwread_epd(addrepd)
    f_dwwrite_epd(addrepd, value)
    patcharr.set(patchsize, addrepd)
    patchsize += 1
    patcharr.set(patchsize, origvalue)
    patchsize += 1

@c.EUDFunc
def f_unpatchall():
    global patchsize
    if cs.EUDWhile()(patchsize >= 2):
        patchsize -= 1
        origvalue = patcharr.get(patchsize)
        patchsize -= 1
        addrepd = patcharr.get(patchsize)
        f_dwwrite_epd(addrepd, origvalue)
    cs.EUDEndWhile()
