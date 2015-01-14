from .muldiv import f_mul, f_div
from .bitwise import (
    f_bitand,
    f_bitor,
    f_bitxor,
    f_bitnand,
    f_bitnor,
    f_bitnxor,
    f_bitnot,
    f_bitlshift,
    f_bitrshift,
    f_bitsplit,
)


from ..varfunc import EUDVariable

def DefClsMethod(name, f):
    f.__name__ = 'EUDVariable.%s' % name
    setattr(EUDVariable, name, f)

def DefOperator(name, f):
    DefClsMethod(name, f)

    def iop(self, rhs):
        self << f(self, rhs)
        return self
    DefClsMethod('__i%s' % name[2:], iop)

    def rop(self, lhs):
        return f(lhs, self)
    DefClsMethod('__r%s' % name[2:], rop)

DefOperator('__mul__', lambda x, y: f_mul(x, y))
DefOperator('__floordiv__', lambda x, y: f_div(x, y)[0])
DefOperator('__mod__', lambda x, y: f_div(x, y)[1])
DefOperator('__and__', lambda x, y: f_bitand(x, y))
DefOperator('__or__', lambda x, y: f_bitor(x, y))
DefOperator('__xor__', lambda x, y: f_bitxor(x, y))
