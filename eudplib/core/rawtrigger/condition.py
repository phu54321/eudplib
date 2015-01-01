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

from ..allocator import Expr, Evaluate, IsValidExpr


class Condition(Expr):
    '''
    Condition class.

    Memory layout:

     ======  =============  ========  ===========
     Offset  Field name     Position  EPD Player
     ======  =============  ========  ===========
       +00   locid           dword0   EPD(cond)+0
       +04   player          dword1   EPD(cond)+1
       +08   amount          dword2   EPD(cond)+2
       +0C   unitid          dword3   EPD(cond)+3
       +0E   comparison
       +0F   condtype
       +10   restype         dword4   EPD(cond)+4
       +11   flags
       +12   internal[2]
     ======  =============  ========  ===========
    '''

    def __init__(self, locid, player, amount, unitid,
                 comparison, condtype, restype, flags):
        super().__init__(self)

        self.locid = locid
        self.player = player
        self.amount = amount
        self.unitid = unitid
        self.comparison = comparison
        self.condtype = condtype
        self.restype = restype
        self.flags = flags

        self.parenttrg = None
        self.condindex = None

    def Disable(self):
        self.flags |= 2

    # -------

    def CheckArgs(self):
        assert self.locid is None or IsValidExpr(self.locid), (
            'Invalid arg %s' % self.locid)
        assert self.player is None or IsValidExpr(self.player), (
            'Invalid arg %s' % self.player)
        assert self.amount is None or IsValidExpr(self.amount), (
            'Invalid arg %s' % self.amount)
        assert self.unitid is None or IsValidExpr(self.unitid), (
            'Invalid arg %s' % self.unitid)
        assert self.comparison is None or IsValidExpr(self.comparison), (
            'Invalid arg %s' % self.comparison)
        assert self.condtype is None or IsValidExpr(self.condtype), (
            'Invalid arg %s' % self.condtype)
        assert self.restype is None or IsValidExpr(self.restype), (
            'Invalid arg %s' % self.restype)
        assert self.flags is None or IsValidExpr(self.flags), (
            'Invalid arg %s' % self.flags)
        return True

    def SetParentTrigger(self, trg, index):
        assert self.parenttrg is None, (
            'Condition cannot be shared by two triggers. '
            'Deep copy each conditions')

        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 16, 'WTF'

        self.parenttrg = trg
        self.condindex = index

    def Evaluate(self):
        assert self.parenttrg is not None, 'Orphan condition'
        return Evaluate(self.parenttrg) + 8 + self.condindex * 20

    def WritePayload(self, pbuffer):
        pbuffer.WritePack(
            'IIIHBBBBH',
            self.locid,
            self.player,
            self.amount,
            self.unitid,
            self.comparison,
            self.condtype,
            self.restype,
            self.flags,
            0
        )
