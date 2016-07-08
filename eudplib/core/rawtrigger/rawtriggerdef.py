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

from ..eudobj import EUDObject
from .triggerscope import NextTrigger, _RegisterTrigger
from .condition import Condition
from .action import Action
from eudplib import utils as ut


# Trigger counter thing

_trgCounter = 0


def GetTriggerCounter():
    return _trgCounter


# Aux

def _bool2Cond(x):
    if x is True:
        return Condition(0, 0, 0, 0, 0, 22, 0, 0)  # Always
    elif x is False:
        return Condition(0, 0, 0, 0, 0, 23, 0, 0)  # Never
    else:
        return x


def Disabled(arg):
    """Disable condition or action"""
    arg.Disabled()


# RawTrigger

class RawTrigger(EUDObject):

    def __init__(
            self,
            prevptr=None,
            nextptr=None,
            conditions=None,
            actions=None,
            preserved=True
    ):
        super().__init__()

        global _trgCounter
        _trgCounter += 1

        _RegisterTrigger(self)  # This should be called before (1)

        if prevptr is None:
            prevptr = 0

        if nextptr is None:
            nextptr = NextTrigger()  # (1)

        if conditions is None:
            conditions = []

        if actions is None:
            actions = []

        conditions = ut.FlattenList(conditions)
        actions = ut.FlattenList(actions)

        ut.ep_assert(len(conditions) <= 16, 'Too many conditions')
        ut.ep_assert(len(actions) <= 64, 'Too many actions')
        ut.ep_assert(isinstance(preserved, bool), 'preserved should be bool')

        conditions = list(map(_bool2Cond, conditions))
        self._prevptr = prevptr
        self._nextptr = nextptr
        self._conditions = conditions
        self._actions = actions

        for i, cond in enumerate(self._conditions):
            ut.ep_assert(isinstance(cond, Condition))
            try:
                cond.CheckArgs()
            except ut.EPError:
                print('Error on condition %d' % i)
                raise

            cond.SetParentTrigger(self, i)

        for i, act in enumerate(self._actions):
            ut.ep_assert(isinstance(act, Action))
            try:
                act.CheckArgs()
            except ut.EPError:
                print('Error on action %d' % i)
                raise

            act.SetParentTrigger(self, i)

        self.preserved = preserved

    def GetNextPtrMemory(self):
        return self + 4

    def GetDataSize(self):
        return 2408

    def WritePayload(self, pbuffer):
        pbuffer.WriteDword(self._prevptr)
        pbuffer.WriteDword(self._nextptr)

        # Conditions
        for cond in self._conditions:
            cond.WritePayload(pbuffer)

        if len(self._conditions) != 16:
            pbuffer.WriteBytes(bytes(20))
            pbuffer.WriteSpace(20 * (15 - len(self._conditions)))

        # Actions
        for act in self._actions:
            act.WritePayload(pbuffer)

        if len(self._actions) != 64:
            pbuffer.WriteBytes(bytes(32))
            pbuffer.WriteSpace(32 * (63 - len(self._actions)))

        # Preserved flag

        if self.preserved:
            pbuffer.WriteDword(4)
        else:
            pbuffer.WriteDword(0)

        pbuffer.WriteSpace(27)
        pbuffer.WriteByte(0)
