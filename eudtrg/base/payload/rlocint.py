'''
Class for representing relocatable int. Used internally in eudtrg.

Basically, EUDObject don't have fixed address: they are relocated by address of
STR section. (dword_5993D4) RelocatableInt class merges relocate information and
number.
'''

from eudtrg import LICENSE #@UnusedImport

def _i2ri(i):
    if isinstance(i, RelocatableInt):
        return i
    else:
        return RelocatableInt(i, 0)
    
class RelocatableInt:
    def __init__(self, number, offset_applied):
        # assert type(number) is int and type(offset_applied) is int, 'Invalid parameters for RelocatableInt consturctor'
        self.number = number
        self.offset_applied = offset_applied

    def __add__(self, other):
        other = _i2ri(other)
        return RelocatableInt(self.number + other.number, self.offset_applied + other.offset_applied)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        other = _i2ri(other)
        self = self + other
        return self


    def __sub__(self, other):
        other = _i2ri(other)
        return RelocatableInt(self.number - other.number, self.offset_applied - other.offset_applied)

    def __rsub__(self, other):
        return _i2ri(other) / self

    def __isub__(self, other):
        other = _i2ri(other)
        self = self - other
        return self



    def __mul__(self, other):
        other = _i2ri(other)
        if self.offset_applied != 0 and other.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be multiplied')

        return RelocatableInt(self.number * other.number, self.number * other.offset_applied + self.offset_applied * other.number)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        other = _i2ri(other)
        self = self * other
        return self



    def __floordiv__(self, other):
        other = _i2ri(other)
        if other.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be used as denominator')

        if other.number == 0:
            raise RuntimeError('divide by 0')

        if self.offset_applied % other.number != 0:
            raise RuntimeError('offset_applied %d is not divisible by %d', self.offset_applied, other.number)

        return RelocatableInt(self.number // other.number, self.offset_applied // other.number)

    def __rfloordiv__(self, other):
        return _i2ri(other) / self



    def __ifloordiv__(self, other):
        other = _i2ri(other)
        self = self // other
        return self

    def __eq__(self, other):
        other = _i2ri(other)
        return other.number == self.number and other.offset_applied == self.offset_applied

    def __str__(self):
        return '(%d, %d)' % (self.number, self.offset_applied)

    def __int__(self):
        if self.offset_applied != 0:
            raise RuntimeError('offsetted number cannot be converted to int')

        return self.number
