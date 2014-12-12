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
        See :mod:`eudtrg.base.stocktrg` for stock actions list.
        '''
        super().__init__(self)

        assert locid1 is None or IsValidSCMemAddr(locid1), (
            'Invalid arg %s' % locid1)
        assert strid is None or IsValidSCMemAddr(strid), (
            'Invalid arg %s' % strid)
        assert wavid is None or IsValidSCMemAddr(wavid), (
            'Invalid arg %s' % wavid)
        assert time is None or IsValidSCMemAddr(time), (
            'Invalid arg %s' % time)
        assert player1 is None or IsValidSCMemAddr(player1), (
            'Invalid arg %s' % player1)
        assert player2 is None or IsValidSCMemAddr(player2), (
            'Invalid arg %s' % player2)
        assert unitid is None or IsValidSCMemAddr(unitid), (
            'Invalid arg %s' % unitid)
        assert acttype is None or IsValidSCMemAddr(acttype), (
            'Invalid arg %s' % acttype)
        assert amount is None or IsValidSCMemAddr(amount), (
            'Invalid arg %s' % amount)
        assert flags is None or IsValidSCMemAddr(flags), (
            'Invalid arg %s' % flags)

        self._locid1 = locid1
        self._strid = strid
        self._wavid = wavid
        self._time = time
        self._player1 = player1
        self._player2 = player2
        self._unitid = unitid
        self._acttype = acttype
        self._amount = amount
        self._flags = flags

        self._parenttrg = None
        self._actindex = None

    def Disable(self):
        self._flags |= 2

    def SetParentTrigger(self, trg, index):
        assert self._parenttrg is None, (
            'Action cannot be shared by two triggers.'
            'Deep copy each conditions')

        assert trg is not None, 'Trigger should not be null.'
        assert 0 <= index < 64, 'WTF'

        self._parenttrg = trg
        self._actindex = index

    # -------

    def Evaluate(self):
        return Evaluate(self._parenttrg) + 8 + 320 + 32 * self._actindex

    def WritePayload(self, pbuffer):
        pbuffer.WritePack(
            'IIIIIIHBBBBH',
            self._locid1,
            self._strid,
            self._wavid,
            self._time,
            self._player1,
            self._player2,
            self._unitid,
            self._acttype,
            self._amount,
            self._flags,
            0,
            0
        )
