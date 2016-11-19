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


class ExprProxy:

    ''' Class which can contain both constxpr and eudvariable '''

    def __init__(self, initval):
        self._value = initval

    def getValue(self):
        return self._value

    def __hash__(self):
        return id(self)

    # Proxy arithmetic operators
    def __lshift__(self, other):
        return self._value << other

    def __add__(self, other):
        return self._value + other

    def __radd__(self, other):
        return other + self._value

    def __sub__(self, other):
        return self._value - other

    def __rsub__(self, other):
        return other - self._value

    def __mul__(self, k):
        return self._value * k

    def __rmul__(self, k):
        return k * self._value

    def __floordiv__(self, k):
        return self._value // k

    def __rfloordiv__(self, other):
        return k // self._value

    def __and__(self, other):
        return self._value & k

    def __rand__(self, other):
        return other & self._value

    def __or__(self, k):
        return self._value | other

    def __ror__(self, k):
        return other | self._value

    def __xor__(self, other):
        return self._value ^ other

    def __rxor__(self, other):
        return other ^ self._value

    def __neg__(self):
        return -self._value

    def __invert__(self):
        return ~self._value

    def __bool__(self):
        return bool(self._value)

    # Proxy comparison operator

    def __eq__(self, k):
        return self._value == k

    def __ne__(self, k):
        return self._value != k

    def __le__(self, other):
        return self._value <= other

    def __lt__(self, other):
        return self._value < other

    def __ge__(self, other):
        return self._value >= other

    def __gt__(self, other):
        return self._value > other

    # TODO: add inplace operators

    # Proxy other methods
    def __getattr__(self, name):
        return getattr(self._value, name)


def unProxy(x):
    try:
        return unProxy(x.getValue())
    except AttributeError:
        return x
