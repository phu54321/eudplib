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

import weakref
import collections

from .. import rawtrigger as bt
from ..allocator import (
    Evaluate,
    Forward,
    ConstExpr,
    IsConstExpr,
)

from ...utils import (
    EPD,
    ExprProxy
)

from .eudv import EUDVariable, SeqCompute, IsEUDVariable
from .vbuf import GetCurrentVariableBuffer


class EUDVArrayData(ConstExpr):
    def __init__(self, initvars):
        super().__init__(self)
        self._initvars = initvars

        # Process initvars
        variableItems = []
        for i, var in enumerate(initvars):
            if IsEUDVariable(var):
                initvars[i] = 0
                variableItems.append((i, var))

        if variableItems:
            SeqCompute(
                [(EPD(self + 344 + 60 * i), bt.SetTo, var)
                 for i, var in variableItems
                 ])

        self._vdict = weakref.WeakKeyDictionary()

    def Evaluate(self):
        evb = GetCurrentVariableBuffer()
        if evb not in self._vdict:
            variables = [evb.CreateVarTrigger(ival) for ival in self._initvars]
            self._vdict[evb] = variables[0]

        return Evaluate(self._vdict[evb])


class EUDVArray(ExprProxy):
    def __init__(self, initvars, basetype=None):
        if isinstance(initvars, int):
            initvars = [0] * initvars

        if isinstance(initvars, collections.Iterable):
            baseobj = EUDVArrayData(initvars)

        elif IsConstExpr(initvars):
            baseobj = initvars
        else:
            baseobj = EUDVariable()
            baseobj << initvars

        super().__init__(baseobj)
        self._epd = EPD(self)
        self._basetype = basetype

    def getItemPtr(self, i):
        return self + 60 * i

    def getItemEPD(self, i):
        return self._epd + 15 * i

    def get(self, i):
        # This function is hand-optimized

        ret = EUDVariable()
        itemptr = self.getItemPtr(i)
        itemepd = self.getItemEPD(i)

        vtproc = Forward()
        nptr = Forward()
        a0, a1, a2 = Forward(), Forward(), Forward()

        SeqCompute([
            (EPD(vtproc + 4), bt.SetTo, itemptr),
            (EPD(a0 + 16), bt.SetTo, itemepd + (8 + 320 + 16) // 4),
            (EPD(a1 + 16), bt.SetTo, itemepd + (8 + 320 + 24) // 4),
            (EPD(a2 + 16), bt.SetTo, itemepd + 1),
        ])

        vtproc << bt.RawTrigger(
            nextptr=0,
            actions=[
                a0 << bt.SetDeaths(0, bt.SetTo, EPD(ret.getValueAddr()), 0),
                a1 << bt.SetDeaths(0, bt.SetTo, 0x072D0000, 0),
                a2 << bt.SetDeaths(0, bt.SetTo, nptr, 0),
            ]
        )

        nptr << bt.NextTrigger()
        if self._basetype:
            ret = self._basetype(ret)
        return ret

    def set(self, i, value):
        itemepd = self.getItemEPD(i)
        a0, t = Forward(), Forward()
        SeqCompute([
            (EPD(a0 + 16), bt.SetTo, itemepd + (8 + 320 + 20) // 4),
            (EPD(a0 + 20), bt.SetTo, value),
        ])
        t << bt.RawTrigger(
            actions=[
                a0 << bt.SetDeaths(0, bt.SetTo, 0, 0),
            ]
        )

    def __getitem__(self, i):
        return self.get(i)

    def __setitem__(self, i, value):
        return self.set(i, value)
