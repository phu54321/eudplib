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

from .. import (
    core as c,
    ctrlstru as cs,
    utils as ut
)

from .eudarray import EUDArray


class ObjPool:
    def __init__(self, basetype, size):
        self.basetype = basetype
        self.size = size
        self.remaining = c.EUDVariable(size)

        fieldn = len(basetype._fields_)
        objects = [c.EUDVArray(fieldn)([0] * fieldn) for _ in range(size)]
        self.data = EUDArray(objects)

    def full(self):
        return self.remaining == 0

    @c.EUDMethod
    def _alloc(self):
        """ Allocate one object from pool """
        if cs.EUDIf()(self.full()):
            c.EUDReturn(0)
        cs.EUDEndIf()

        self.remaining -= 1
        data = self.data[self.remaining]
        return data

    def alloc(self, *args, **kwargs):
        data = self._alloc()
        data = self.basetype.cast(data)
        data.constructor(*args, **kwargs)
        return data

    @c.EUDMethod
    def free(self, data):
        data = self.basetype.cast(data)
        data.destructor()
        self.data[self.remaining] = data
        self.remaining += 1


poolList = {}


def SetPoolSize(t, size):
    try:
        ut.ep_assert(poolList[t].size == size,
                     "Cannot change size of the global pool")
    except KeyError:
        poolList[t] = ObjPool(t, size)


def Pool(t):
    return poolList[t]
