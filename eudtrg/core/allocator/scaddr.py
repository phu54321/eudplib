import traceback
from . import rlocint


class SCMemAddr:

    def __init__(self, baseobj, offset=0, rlocmode=4):
        self.baseobj = baseobj
        self.offset = offset
        self.rlocmode = rlocmode

    def Evaluate(self):
        assert self.rlocmode in [1, 4]
        return Evaluate(self.baseobj) * (self.rlocmode // 4) + self.offset

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


class Forward(SCMemAddr):

    ''' Class for late definition
    '''

    def __init__(self):
        super().__init__(self)
        self._expr = None
        # self._traceback = traceback.extract_stack()

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
        assert self._expr is not None, (
            'Forward not properly initialized\n'
            'Forward initialized at :\n'
            + (
                '--| ' +
                ''.join(traceback.format_list(self._traceback)()[:-1])
                .replace('\n', '\n  | ')
            )
        )

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
