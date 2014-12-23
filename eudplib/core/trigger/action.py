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

from ..allocator import Expr, Evaluate, IsValidSCMemAddr


class Action(Expr):
    '''
    Action class.

    Memory layout.

     ======  ============= ========  ==========
     Offset  Field Name    Position  EPD Player
     ======  ============= ========  ==========
       +00   locid1         dword0   EPD(act)+0
       +04   strid          dword1   EPD(act)+1
       +08   wavid          dword2   EPD(act)+2
       +0C   time           dword3   EPD(act)+3
       +10   player1        dword4   EPD(act)+4
       +14   player2        dword5   EPD(act)+5
       +18   unitid         dword6   EPD(act)+6
       +1A   acttype
       +1B   amount
       +1C   flags          dword7   EPD(act)+7
       +1D   internal[3
     ======  ============= ========  ==========
    '''

    def __init__(self, locid1, strid, wavid, time, player1, player2,
                 unitid, acttype, amount, flags):
        '''
        See :mod:`eudplib.base.stocktrg` for stock actions list.
        '''
        super().__init__(self)

        self.locid1 = locid1
        self.strid = strid
        self.wavid = wavid
        self.time = time
        self.player1 = player1
        self.player2 = player2
        self.unitid = unitid
        self.acttype = acttype
        self.amount = amount
        self.flags = flags

        self.parenttrg = None
        self.actindex = None

    def Disable(self):
        self.flags |= 2

    # -------

    def CheckArgs(self):
        assert self.locid1 is None or IsValidSCMemAddr(self.locid1), (
            'Invalid arg %s' % self.locid1)
        assert self.strid is None or IsValidSCMemAddr(self.strid), (
            'Invalid arg %s' % self.strid)
        assert self.wavid is None or IsValidSCMemAddr(self.wavid), (
            'Invalid arg %s' % self.wavid)
        assert self.time is None or IsValidSCMemAddr(self.time), (
            'Invalid arg %s' % self.time)
        assert self.player1 is None or IsValidSCMemAddr(self.player1), (
            'Invalid arg %s' % self.player1)
        assert self.player2 is None or IsValidSCMemAddr(self.player2), (
            'Invalid arg %s' % self.player2)
        assert self.unitid is None or IsValidSCMemAddr(self.unitid), (
            'Invalid arg %s' % self.unitid)
        assert self.acttype is None or IsValidSCMemAddr(self.acttype), (
            'Invalid arg %s' % self.acttype)
        assert self.amount is None or IsValidSCMemAddr(self.amount), (
            'Invalid arg %s' % self.amount)
        assert self.flags is None or IsValidSCMemAddr(self.flags), (
            'Invalid arg %s' % self.flags)
        return True

    def SetParentTrigger(self, trg, index):
        assert self.parenttrg is None, (
            'Action cannot be shared by two triggers.'
            'Deep copy each conditions')

        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 64, 'WTF'

        self.parenttrg = trg
        self.actindex = index

    def Evaluate(self):
        return Evaluate(self.parenttrg) + 8 + 320 + 32 * self.actindex

    def WritePayload(self, pbuffer):
        pbuffer.WritePack(
            'IIIIIIHBBBBH',
            self.locid1,
            self.strid,
            self.wavid,
            self.time,
            self.player1,
            self.player2,
            self.unitid,
            self.acttype,
            self.amount,
            self.flags,
            0,
            0
        )
