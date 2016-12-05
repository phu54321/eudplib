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
)

from .eudarray import EUDArray


class ObjPool(c.EUDStruct):
    _fields_ = [
        ('data', EUDArray),
        'remaining',
        'size'
    ]

    def __init__(self, size, basetype=None):
        objects = [basetype() for _ in range(size)]
        super().__init__([
            EUDArray(objects),
            size,
            size
        ])
        self._basetype = basetype

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

    def alloc(self):
        data = self._alloc()
        if self._basetype:
            data = self._basetype(data)
        return data

    @c.EUDMethod
    def free(self, data):
        self.data[self.remaining] = data
        self.remaining += 1

    def clone(self):
        raise RuntimeError('Pool is not clonable')

    def deepcopy(self):
        raise RuntimeError('Pool is not copyable')
