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


class RlocInt:

    """Relocatable int"""

    def __init__(self, offset, rlocmode):
        self.offset, self.rlocmode = offset, rlocmode

    def __add__(self, other):
        other = toRlocInt(other)
        return RlocInt(
            self.offset + other.offset,
            self.rlocmode + other.rlocmode
        )

    def __sub__(self, other):
        other = toRlocInt(other)
        return RlocInt(
            self.offset - other.offset,
            self.rlocmode - other.rlocmode
        )

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return toRlocInt(other) - self

    def __mul__(self, other):
        other = toRlocInt(other)
        ut.ep_assert(
            self.rlocmode == 0 or other.rlocmode == 0,
            'Cannot multiply two non-const RlocInts'
        )

        return RlocInt(
            self.offset * other.offset,
            self.rlocmode * other.offset + self.offset * other.rlocmode
        )

    def __floordiv__(self, other):
        other = toRlocInt(other)
        ut.ep_assert(
            other.rlocmode == 0,
            'Cannot divide RlocInt with non-const'
        )
        ut.ep_assert(other.offset != 0, 'Divide by zero')
        ut.ep_assert(
            (self.rlocmode == 0) or
            (self.rlocmode % other.offset == 0 and
             self.offset % other.offset == 0),
            'RlocInt not divisible by %d' % other.offset
        )
        return RlocInt(
            self.offset // other.offset,
            self.rlocmode // other.offset
        )

    def __str__(self):
        return 'Rlocint(0x%08X, %d)' % (self.offset, self.rlocmode)

    def __repr__(self):
        return str(self)


def toRlocInt(x):
    """Convert int/RlocInt to rlocint"""

    if isinstance(x, RlocInt):
        return x

    else:
        return RlocInt(x, 0)
