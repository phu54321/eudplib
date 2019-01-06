#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2019 Armoha

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

from .. import rawtrigger as bt
from ...utils import EPD
from .eudv import EUDVariable, VariableTriggerForward


class EUDXVariable(EUDVariable):

    def __init__(self, initval=0, mask=~0):
        self._vartrigger = VariableTriggerForward(initval, mask)
        self._varact = self._vartrigger + (8 + 320)
        self._rvalue = False

    # -------

    def SetMask(self, value):
        return bt.SetDeaths(EPD(self._varact), bt.SetTo, value, 0)

    def AddMask(self, value):
        return bt.SetDeaths(EPD(self._varact), bt.Add, value, 0)

    def SubtractMask(self, value):
        return bt.SetDeaths(EPD(self._varact), bt.Subtract, value, 0)

    # -------

    def SetMaskX(self, value, mask):
        return bt.SetDeathsX(EPD(self._varact), bt.SetTo, value, 0, mask)

    def AddMaskX(self, value, mask):
        return bt.SetDeathsX(EPD(self._varact), bt.Add, value, 0, mask)

    def SubtractMaskX(self, value, mask):
        return bt.SetDeathsX(EPD(self._varact), bt.Subtract, value, 0, mask)

    # -------

    def MaskAtLeast(self, value):
        return bt.Deaths(EPD(self._varact), bt.AtLeast, value, 0)

    def MaskAtMost(self, value):
        return bt.Deaths(EPD(self._varact), bt.AtMost, value, 0)

    def MaskExactly(self, value):
        return bt.Deaths(EPD(self._varact), bt.Exactly, value, 0)

    # -------

    def MaskAtLeastX(self, value, mask):
        return bt.DeathsX(EPD(self._varact), bt.AtLeast, value, mask, 0)

    def MaskAtMostX(self, value, mask):
        return bt.DeathsX(EPD(self._varact), bt.AtMost, value, mask, 0)

    def MaskExactlyX(self, value, mask):
        return bt.DeathsX(EPD(self._varact), bt.Exactly, value, mask, 0)
