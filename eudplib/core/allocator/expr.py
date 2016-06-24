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

from . import rlocint
from .handle import Handle
from eudplib import utils as ut


class Expr(Handle):

    ''' Class for general expression with rlocints.
    '''

    def __init__(self, baseobj, offset=0, rlocmode=4):
        self.baseobj = baseobj
        self.offset = offset
        self.rlocmode = rlocmode

    def Evaluate(self):
        return Evaluate(self.baseobj) // 4 * self.rlocmode + self.offset

    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Expr(self.baseobj, self.offset + other, self.rlocmode)

    def __radd__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Expr(self.baseobj, self.offset + other, self.rlocmode)

    def __sub__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        if isinstance(other, Expr):
            ut.ep_assert(
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode,
                'Cannot subtract between addresses btw two objects'
            )
            return self.offset - other.offset

        else:
            return Expr(self.baseobj, self.offset - other, self.rlocmode)

    def __rsub__(self, other):
        if isinstance(other, Expr):
            ut.ep_assert(
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode,
                'Cannot subtract between addresses btw two distinct objects'
            )
            return other.offset - self.offset

        elif not isinstance(other, int):
            return NotImplemented

        else:
            return Expr(self.baseobj, other - self.offset, -self.rlocmode)

    def __mul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return Expr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __rmul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return Expr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __floordiv__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        ut.ep_assert(
            (self.rlocmode == 0) or
            (self.rlocmode % k == 0 and self.offset % k == 0),
            'Address not divisible'
        )
        return Expr(self.baseobj, self.offset // k, self.rlocmode // k)


class Forward(Expr):

    '''Class for forward definition.
    '''

    def __init__(self):
        super().__init__(self)
        self._expr = None

    def __lshift__(self, expr):
        ut.ep_assert(
            self._expr is None,
            'Reforwarding without reset is not allowed'
        )
        ut.ep_assert(expr is not None, 'Cannot forward to None')
        self._expr = expr
        return expr

    def IsSet(self):
        return self._expr is not None

    def Reset(self):
        self._expr = None

    def Evaluate(self):
        ut.ep_assert(self._expr is not None, 'Forward not initialized')
        return Evaluate(self._expr)


def Evaluate(x):
    '''
    Evaluate expressions
    '''
    if isinstance(x, int):
        return rlocint.RlocInt(x, 0)
    try:
        return x.Evaluate()
    except AttributeError:
        return x


def IsValidExpr(x):
    return isinstance(x, Expr) or isinstance(x, int)
