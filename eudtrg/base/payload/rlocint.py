
"""
Relocatable int. Used internally in eudtrg.
"""

from eudtrg import LICENSE #@UnusedImport

class RelocatableInt:
    def __init__(self, number, offset_applied):
        # assert type(number) is int and type(offset_applied) is int, 'Invalid parameters for RelocatableInt consturctor'
        self.number = number
        self.offset_applied = offset_applied

    def __add__(self, other):
        return RelocatableInt(self.number + other.number, self.offset_applied + other.offset_applied)

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        return RelocatableInt(self.number - other.number, self.offset_applied - other.offset_applied)

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        if self.offset_applied != 0 and other.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be multiplied')

        return RelocatableInt(self.number * other.number, self.number * other.offset_applied + self.offset_applied * other.number)

    def __imul__(self, other):
        self = self * other
        return self

    def __floordiv__(self, other):
        if other.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be used as denominator')

        if other.number == 0:
            raise RuntimeError('divide by 0')

        if self.offset_applied % other.number != 0:
            raise RuntimeError('offset_applied %d is not divisible by %d', self.offset_applied, other.number)

        return RelocatableInt(self.number // other.number, self.offset_applied // other.number)

    def __ifloordiv__(self, other):
        self = self // other
        return self

    def __eq__(self, other):
        return other.number == self.number and other.offset_applied == self.offset_applied

    def __str__(self):
        return '(%d, %d)' % (self.number, self.offset_applied)

    def __int__(self):
        if self.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be used as denominator')

        return self.number
