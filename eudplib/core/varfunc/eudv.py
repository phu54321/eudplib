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
import traceback

from .. import rawtrigger as bt
from ..allocator import (
    Evaluate,
    Forward,
    Expr,
    IsValidExpr
)
from ..utils import (
    EPD,
    List2Assignable
)
from .vbase import VariableBase
from .vbuf import GetCurrentVariableBuffer


class VariableTriggerForward(Expr):
    def __init__(self):
        super().__init__(self)
        self._expr = weakref.WeakKeyDictionary()

    def Evaluate(self):
        evb = GetCurrentVariableBuffer()
        if evb not in self._expr:
            self._expr[evb] = evb.CreateVarTrigger()
        return Evaluate(self._expr[evb])


class EUDVariable(VariableBase):
    '''
    Full variable.
    '''

    def __init__(self):
        self._vartrigger = VariableTriggerForward()
        self._varact = self._vartrigger + (8 + 320)

    def GetVTable(self):
        return self._vartrigger

    def GetVariableMemoryAddr(self):
        return self._varact + 20

    # -------

    def QueueAssignTo(self, dest):
        try:
            dest = EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            bt.SetDeaths(EPD(self._varact + 16), bt.SetTo, dest, 0),
            bt.SetDeaths(EPD(self._varact + 24), bt.SetTo, 0x072D0000, 0),
        ]

    def QueueAddTo(self, dest):
        try:
            dest = EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            bt.SetDeaths(EPD(self._varact + 16), bt.SetTo, dest, 0),
            bt.SetDeaths(EPD(self._varact + 24), bt.SetTo, 0x082D0000, 0),
        ]

    def QueueSubtractTo(self, dest):
        try:
            dest = EPD(dest.GetVariableMemoryAddr())
        except AttributeError:
            pass

        return [
            bt.SetDeaths(EPD(self._varact + 16), bt.SetTo, dest, 0),
            bt.SetDeaths(EPD(self._varact + 24), bt.SetTo, 0x092D0000, 0),
        ]

    # -------

    def Assign(self, other):
        SeqCompute((
            (self, bt.SetTo, other),
        ))
        return self

    def __lshift__(self, other):
        self.Assign(other)

    def __iadd__(self, other):
        SeqCompute(((self, bt.Add, other),))

    def __isub__(self, other):
        self << self - other

    # -------

    def __add__(self, other):
        t = EUDVariable()
        SeqCompute([
            (t, bt.SetTo, self),
            (t, bt.Add, other)
        ])
        return t

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        t = EUDVariable()
        SeqCompute([
            (t, bt.SetTo, 0xffffffff),
            (t, bt.Subtract, other),
            (t, bt.Add, 1),
            (t, bt.Add, self),
        ])
        return t

    def __rsub__(self, other):
        t = EUDVariable()
        SeqCompute([
            (t, bt.SetTo, 0xffffffff),
            (t, bt.Subtract, self),
            (t, bt.Add, 1),
            (t, bt.Add, other),
        ])
        return t

    # -------

    def __eq__(self, other):
        if IsValidExpr(other):
            return self.Exactly(other)

        else:
            return (self - other).Exactly(0)

    def __le__(self, other):
        if IsValidExpr(other):
            return self.AtMost(other)

        else:
            t = EUDVariable()
            SeqCompute((
                (t, bt.SetTo, self),
                (t, bt.Subtract, other)
            ))
            return t.Exactly(0)

    def __ge__(self, other):
        if IsValidExpr(other):
            return self.AtLeast(other)

        else:
            t = EUDVariable()
            SeqCompute((
                (t, bt.SetTo, other),
                (t, bt.Subtract, self)
            ))
            return t.Exactly(0)

    def __lt__(self, other):
        if isinstance(other, int) and other <= 0:
            print('[Warning] No unsigned number can be leq than %d' % other)
            traceback.print_stack()
            return [bt.Never()]  # No unsigned number is less than 0

        if IsValidExpr(other):
            return self.AtMost(other - 1)

        else:
            t = EUDVariable()
            SeqCompute((
                (t, bt.SetTo, self),
                (t, bt.Add, 1),
                (t, bt.Subtract, other)
            ))
            return t.Exactly(0)

    def __gt__(self, other):
        if isinstance(other, int) and other >= 0xFFFFFFFF:
            print('[Warning] No unsigned int can be greater than %d' % other)
            traceback.print_stack()
            return [bt.Never()]  # No unsigned number is less than 0

        if IsValidExpr(other):
            return self.AtLeast(other + 1)

        else:
            t = EUDVariable()
            SeqCompute((
                (t, bt.SetTo, self),
                (t, bt.Subtract, 1),
                (t, bt.Subtract, other)
            ))
            return t.AtLeast(1)


def _VProc(v, actions):
    nexttrg = Forward()

    bt.RawTrigger(
        nextptr=v.GetVTable(),
        actions=[actions] + [bt.SetNextPtr(v.GetVTable(), nexttrg)]
    )

    nexttrg << bt.NextTrigger()


# From vbuffer.py
def EUDCreateVariables(varn):
    return List2Assignable([EUDVariable() for _ in range(varn)])


# -------


def SeqCompute(assignpairs):
    actionset = []

    def FlushActionSet():
        nonlocal actionset
        if actionset:
            bt.RawTrigger(actions=actionset)
            actionset.clear()

    for dst, mdt, src in assignpairs:
        try:
            dstepd = EPD(dst.GetVariableMemoryAddr())
        except AttributeError:
            dstepd = dst

        if isinstance(src, EUDVariable):
            FlushActionSet()

            if mdt == bt.SetTo:
                _VProc(src, [
                    src.QueueAssignTo(dstepd)
                ])

            elif mdt == bt.Add:
                _VProc(src, [
                    src.QueueAddTo(dstepd)
                ])

            elif mdt == bt.Subtract:
                _VProc(src, [
                    src.QueueSubtractTo(dstepd)
                ])

        else:
            actionset.append(bt.SetDeaths(dstepd, mdt, src, 0))
            if len(actionset) == 64:
                FlushActionSet()

    FlushActionSet()
