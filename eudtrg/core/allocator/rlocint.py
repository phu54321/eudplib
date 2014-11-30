class RlocInt:

    def __init__(self, offset, rlocmode):
        assert isinstance(offset, int) and isinstance(rlocmode, int), (
            'Invalid argument for RlocInt constructor')
        self.offset = offset
        self.rlocmode = rlocmode

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
        assert self.rlocmode == 0 or other.rlocmode == 0, (
            'Cannot multiply two non-const RlocInts')

        return RlocInt(
            self.offset * other.offset,
            self.rlocmode * other.offset + self.offset * other.rlocmode
        )

    def __floordiv__(self, other):
        other = toRlocInt(other)
        assert other.rlocmode == 0, (
            'Cannot divide RlocInt with non-const')
        assert other.offset != 0, 'Divide by zero'
        assert (
            (self.rlocmode == 0) or
            (self.rlocmode % other.offset == 0 and
             self.offset % other.offset == 0)), (
            'RlocInt not divisible by %d' % other.offset
        )
        return RlocInt(
            self.offset // other.offset,
            self.rlocmode // other.offset
        )

    def __str__(self):
        return 'Rlocint(%d, %d)' % (self.offset, self.rlocmode)

    def __repr__(self):
        return str(self)


def toRlocInt(x):
    if isinstance(x, RlocInt):
        return x

    else:
        return RlocInt(x, 0)
