from . import scalloc as sca


class SCMemAddr:

    def __init__(self, baseobj, offset, rlocmode):
        self.baseobj = baseobj
        self.offset = offset
        self.rlocmode = rlocmode

    def Evaluate(self):
        return sca.GetObjectAddr(self.baseobj) // self.rlocmode + self.offset

    def __add__(self, other):
        assert isinstance(other, int), 'Cannot add address with address'
        return SCMemAddr(self.baseobj, self.offset + other, self.rlocmode)

    def __radd__(self, other):
        assert isinstance(other, int), 'Cannot add address with address'
        return SCMemAddr(self.baseobj, self.offset + other, self.rlocmode)

    def __sub__(self, other):
        assert isinstance(other, int), 'Cannot subtract address from address'
        if isinstance(other, SCMemAddr):
            assert (
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode), (
                'Cannot subtract between addresses btw two objects')
            return self.offset - other.offset

        else:
            return SCMemAddr(self.baseobj, self.offset - other, self.rlocmode)

    def __rsub__(self, other):
        assert isinstance(other, int), 'Cannot subtract address from address'
        if isinstance(other, SCMemAddr):
            assert (
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode), (
                'Cannot subtract between addresses btw two objects')
            return other.offset - self.offset

        else:
            return SCMemAddr(self.baseobj, other - self.offset, -self.rlocmode)

    def __mul__(self, k):
        assert isinstance(k, int), 'Cannot multiply address by address'
        return SCMemAddr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __rmul__(self, k):
        assert isinstance(k, int), 'Cannot multiply address by address'
        return SCMemAddr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __floordiv__(self, k):
        assert isinstance(k, int), 'Cannot multiply address by address'
        assert (
            (self.rlocmode == 0) or
            (self.rlocmode % k == 0 and self.offset % k == 0)), (
            'Address not divisible')
        return SCMemAddr(self.baseobj, self.offset // k, self.rlocmode // k)


def Evaluate(x):
    try:
        return x.Evaluate()
    except AttributeError:
        return x
