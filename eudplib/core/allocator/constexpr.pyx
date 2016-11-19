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

from .rlocint cimport RlocInt_C
from .rlocint import RlocInt, RlocInt_C, toRlocInt
from ... import utils as ut


cdef class ConstExpr:

    ''' Class for general expression with rlocints.
    '''

    cdef public unsigned int offset, rlocmode
    cdef public ConstExpr baseobj

    def __init__(self, baseobj, offset=0, rlocmode=4):
        self.baseobj = baseobj
        self.offset = offset & 0xFFFFFFFF
        self.rlocmode = rlocmode & 0xFFFFFFFF

    cpdef RlocInt_C Evaluate(self):
        return Evaluate(self.baseobj) * self.rlocmode // 4 + self.offset

    # Cython version!

    cpdef ConstExpr adder(self, unsigned int other):
        return ConstExpr(self.baseobj, self.offset + other, self.rlocmode)

    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return ConstExpr(self.baseobj, self.offset + other, self.rlocmode)

    def __radd__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        
        return ConstExpr(self.baseobj, self.offset + other, self.rlocmode)

    def __sub__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return ConstExpr(self.baseobj, self.offset - other, self.rlocmode)

    def __rsub__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return ConstExpr(self.baseobj, other - self.offset, -self.rlocmode)

    def __mul__(self, k):
        if not isinstance(k, int):
            return NotImplemented

        return ConstExpr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __rmul__(self, k):
        if not isinstance(k, int):
            return NotImplemented

        return ConstExpr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __floordiv__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        ut.ep_assert(
            (self.rlocmode == 0) or
            (self.rlocmode % k == 0 and self.offset % k == 0),
            'Address not divisible'
        )
        return ConstExpr(self.baseobj, self.offset // k, self.rlocmode // k)

cdef class ConstExprInt(ConstExpr):
    cdef public RlocInt_C value

    def __init__(self, value):
        super().__init__(None, value, 0)
        self.value = RlocInt_C(value & 0xFFFFFFFF, 0)

    cpdef RlocInt_C Evaluate(self):
        return self.value

cdef class Forward(ConstExpr):

    '''Class for forward definition.
    '''

    cdef public ConstExpr _expr

    def __init__(self):
        super().__init__(self)
        self._expr = None

    def __lshift__(self, expr):
        ut.ep_assert(
            self._expr is None,
            'Reforwarding without reset is not allowed'
        )
        expr = ut.unProxy(expr)
        ut.ep_assert(expr is not None, 'Cannot forward to None')
        if isinstance(expr, int):
            self._expr = ConstExprInt(expr)
        else:
            self._expr = expr
        return expr

    def IsSet(self):
        return self._expr is not None

    def Reset(self):
        self._expr = None

    cpdef RlocInt_C Evaluate(self):
        ut.ep_assert(self._expr is not None, 'Forward not initialized')
        return Evaluate(self._expr)


cpdef RlocInt_C Evaluate(x):
    '''
    Evaluate expressions
    '''
    try:
        return x.Evaluate()
    except AttributeError:
        return toRlocInt(x)


def IsConstExpr(x):
    x = ut.unProxy(x)
    return isinstance(x, int) or hasattr(x, 'Evaluate')
