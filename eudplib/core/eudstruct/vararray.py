#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
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
"""

from .. import rawtrigger as bt
from ..allocator import Forward, ConstExpr, IsConstExpr

from ...utils import EPD, ExprProxy, ep_assert, cachedfunc

from ..variable import EUDVariable, SeqCompute
from ..variable.vbuf import GetCurrentVariableBuffer


@cachedfunc
def EUDVArrayData(size):
    ep_assert(isinstance(size, int))

    class _EUDVArrayData(ConstExpr):
        def __init__(self, initvars):
            super().__init__(self)
            ep_assert(len(initvars) == size, "%d items expected" % size)
            self._initvars = initvars

        def Evaluate(self):
            evb = GetCurrentVariableBuffer()
            if self not in evb._vdict:
                evb.CreateMultipleVarTriggers(self, self._initvars)

            return evb._vdict[self].Evaluate()

    return _EUDVArrayData


@cachedfunc
def EUDVArray(size, basetype=None):
    ep_assert(isinstance(size, int))

    class _EUDVArray(ExprProxy):
        def __init__(self, initvars=None, *, _from=None):
            # Initialization from value
            if _from is not None:
                if IsConstExpr(_from):
                    baseobj = _from

                # Initialization by variable reference
                else:
                    baseobj = EUDVariable()
                    baseobj << _from

            else:
                # Int -> interpret as sequence of 0s
                if initvars is None:
                    initvars = [0] * size

                # For python iterables
                baseobj = EUDVArrayData(size)(initvars)

            super().__init__(baseobj)
            self.dontFlatten = True
            self._epd = EPD(self)
            self._basetype = basetype

        def get(self, i):
            # This function is hand-optimized

            r = EUDVariable()
            vtproc = Forward()
            nptr = Forward()
            a0, a2 = Forward(), Forward()

            SeqCompute(
                [
                    (EPD(vtproc + 4), bt.SetTo, self + 72 * i),
                    (EPD(a0 + 16), bt.SetTo, self._epd + (18 * i + 344 // 4)),
                    (EPD(a2 + 16), bt.SetTo, self._epd + (18 * i + 1)),
                ]
            )

            vtproc << bt.RawTrigger(
                nextptr=0,
                actions=[
                    a0 << bt.SetDeaths(0, bt.SetTo, EPD(r.getValueAddr()), 0),
                    a2 << bt.SetDeaths(0, bt.SetTo, nptr, 0),
                ],
            )

            nptr << bt.NextTrigger()
            if self._basetype:
                r = self._basetype.cast(r)
            return r

        def set(self, i, value):
            # This function is hand-optimized

            a0, t = Forward(), Forward()
            SeqCompute(
                [
                    (EPD(a0 + 16), bt.SetTo, self._epd + (18 * i + 348 // 4)),
                    (EPD(a0 + 20), bt.SetTo, value),
                ]
            )
            t << bt.RawTrigger(actions=[a0 << bt.SetDeaths(0, bt.SetTo, 0, 0)])

        def fill(self, values, *, assert_expected_values_len=None):
            if assert_expected_values_len:
                ep_assert(len(values) == assert_expected_values_len)

            SeqCompute(
                [
                    (EPD(self + 344 + i * 72), bt.SetTo, value)
                    for i, value in enumerate(values)
                ]
            )

        def __getitem__(self, i):
            return self.get(i)

        def __setitem__(self, i, value):
            return self.set(i, value)

    return _EUDVArray
