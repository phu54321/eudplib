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

from eudplib import utils as ut


class EUDObjectView:

    ''' Class for general expression with rlocints.
    '''

    def __init__(self, objAddr):
        if isinstance(objAddr, EUDObjectView):
            objAddr = objAddr.addr()
        self._objEPD = ut.EPD(objAddr)
        self._objAddr = objAddr

    def addr(self):
        return self._objAddr

    def epd(self):
        return self._objEPD

    def __add__(self, other):
        return self.addr() + other

    def __radd__(self, other):
        return other + self.addr()

    def __sub__(self, other):
        return self.addr() - other

    def __rsub__(self, other):
        return other - self.addr()

    def __mul__(self, k):
        return self.addr() * k

    def __rmul__(self, k):
        return k * self.addr()

    def __floordiv__(self, k):
        if k == 4:
            return self.epd() + (0x58A364 // 4)
        return self.addr() // k


def Addr(obj):
    return obj.getBaseObj()
