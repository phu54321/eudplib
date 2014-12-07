#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import rlocint


class SCMemAddr:
    def __init__(self, baseobj, offset=0, rlocmode=4):
        self.baseobj = baseobj
        self.offset = offset
        self.rlocmode = rlocmode

    def Evaluate(self):
        assert self.rlocmode in [1, 4]
        if self.rlocmode == 1:
            return Evaluate(self.baseobj) // 4 + self.offset

        else:
            return Evaluate(self.baseobj) + self.offset

    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return SCMemAddr(self.baseobj, self.offset + other, self.rlocmode)

    def __radd__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return SCMemAddr(self.baseobj, self.offset + other, self.rlocmode)

    def __sub__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        if isinstance(other, SCMemAddr):
            assert (
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode), (
                'Cannot subtract between addresses btw two objects')
            return self.offset - other.offset

        else:
            return SCMemAddr(self.baseobj, self.offset - other, self.rlocmode)

    def __rsub__(self, other):
        if isinstance(other, SCMemAddr):
            assert (
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode), (
                'Cannot subtract between addresses btw two distinct objects')
            return other.offset - self.offset

        elif not isinstance(other, int):
            return NotImplemented

        else:
            return SCMemAddr(self.baseobj, other - self.offset, -self.rlocmode)

    def __mul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return SCMemAddr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __rmul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return SCMemAddr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __floordiv__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        assert (
            (self.rlocmode == 0) or
            (self.rlocmode % k == 0 and self.offset % k == 0)), (
            'Address not divisible')
        return SCMemAddr(self.baseobj, self.offset // k, self.rlocmode // k)


class Forward(SCMemAddr):
    ''' Class for late definition
    '''

    def __init__(self):
        super().__init__(self)
        self._expr = None

    def __lshift__(self, expr):
        assert self._expr is None, 'Reforwarding without reset is not allowed'
        assert expr is not None, 'Cannot forward to None'
        self._expr = expr
        return expr

    def IsSet(self):
        return self._expr is not None

    def Reset(self):
        self._expr = None

    def Evaluate(self):
        assert self._expr is not None, 'Forward not initialized'
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


def IsValidSCMemAddr(x):
    return isinstance(x, SCMemAddr) or isinstance(x, int)
