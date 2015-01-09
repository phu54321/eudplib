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
from .. import ctrlstru as cs
from .. import stdfunc as sf


class EUDArray:
    '''
    Full variable.
    '''

    def __init__(self, len):
        self._dattable = c.Db(4 * len)
        self._varlen = len

    def GetArrayMemory(self):
        return self._dattable

    def GetLength(self):
        return self._varlen

    def get(self, key):
        return sf.f_dwread_epd(c.EPD(self._dattable) + key)

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, item):
        return sf.f_dwwrite_epd(c.EPD(self._dattable) + key, item)

    def __setitem__(self, key, item):
        return self.set(key, item)

