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
from .. import varfunc as vf
from .. import ctrlstru as cs
from .. import stdfunc as sf


class EUDArray:
    '''
    Full variable.
    '''

    def __init__(self, len):
        self._varlist = vf.EUDCreateVariables(len)
        self._varlen = len
        self._debugstring = c.Db(c.u2b('[EUDArray::get] Out of bounds : %s' % hex(id(self))))

    def get(self, key):
        varn = self._varlen
        vlist = self._varlist
        ret = vf.EUDVariable()

        if isinstance(key, int):  # Faster path
            ret << vlist[key]  # May throw indexerror
            return ret

        cs.EUDSwitch(key)
        for i in range(varn):
            cs.EUDSwitchCase(i)
            ret << vlist[i]  # May throw indexerror
            cs.EUDBreak()

        cs.EUDSwitchDefault()  # out of bound
        sf.f_strcpy(0x58D740, self._debugstring)
        cs.EUDJump(0)  # crash

        cs.EUDEndSwitch()

    def set(self, key, item):
        varn = self._varlen
        vlist = self._varlist

        if isinstance(key, int):  # Faster path
            vlist[key] << item
            return

        cs.EUDSwitch(key)
        for i in range(varn):
            cs.EUDSwitchCase(i)
            vlist[i] << item
            cs.EUDBreak()

        cs.EUDSwitchDefault()
        cs.DoActions([
            c.DisplayText('[EUDArray::set] Out of bounds : %s' % self),
            c.Draw()
        ])

        cs.EUDEndSwitch()