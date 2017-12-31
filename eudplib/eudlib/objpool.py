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


def ObjPool(basetype):
    fields = basetype._fields_
    fieldn = len(fields)

    class _ObjPool(c.EUDStruct):
        _fields_ = [
            ('data', EUDArray),
            'remaining',
            'size'
        ]

        def constructor(self, size):
            objects = [c.EUDVArray(fieldn)([0] * fieldn) for _ in range(size)]
            self.data = EUDArray(objects)
            self.remaining = size
            self.size = size

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
            data = basetype.cast(data)
            data.constructor(*args, **kwargs)
            return data

        @c.EUDMethod
        def free(self, data):
            self.data[self.remaining] = data
            self.remaining += 1

        def clone(self):
            raise RuntimeError('Pool is not clonable')

        def deepcopy(self):
            raise RuntimeError('Pool is not copyable')

    return _ObjPool
