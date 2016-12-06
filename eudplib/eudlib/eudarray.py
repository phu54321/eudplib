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

import collections

from .. import core as c
from .. import utils as ut
from .memiof import f_dwread_epd, f_dwwrite_epd


class EUDArrayData(c.EUDObject):
    '''
    Structure for storing multiple values.
    '''

    def __init__(self, arr):
        super().__init__()

        if isinstance(arr, int):
            arrlen = arr
            self._datas = [0] * arrlen
            self._arrlen = arrlen

        else:
            for i, item in enumerate(arr):
                ut.ep_assert(c.IsConstExpr(item), 'Invalid item #%d' % i)
            self._datas = arr
            self._arrlen = len(arr)

    def GetDataSize(self):
        return self._arrlen * 4

    def WritePayload(self, buf):
        for item in self._datas:
            buf.WriteDword(item)

    # --------

    def GetArraySize(self):
        """ Get size of array """
        return self._arrlen

    @c.EUDMethod
    def get(self, key):
        return f_dwread_epd(ut.EPD(self) + key)

    def __getitem__(self, key):
        return self.get(key)

    @c.EUDMethod
    def set(self, key, item):
        return f_dwwrite_epd(ut.EPD(self) + key, item)

    def __setitem__(self, key, item):
        return self.set(key, item)


class EUDArray(ut.ExprProxy):
    def __init__(self, initval):
        if (
            isinstance(initval, int) or
            isinstance(initval, collections.Iterable)
        ):
            dataObj = EUDArrayData(initval)
            self.length = dataObj._arrlen
        else:
            dataObj = initval

        super().__init__(dataObj)
        self._epd = ut.EPD(self)

    def get(self, key):
        return f_dwread_epd(self._epd + key)

    def __getitem__(self, key):
        return self.get(key)

    def set(self, key, item):
        return f_dwwrite_epd(self._epd + key, item)

    def __setitem__(self, key, item):
        return self.set(key, item)
