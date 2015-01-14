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

def DefClsMethod(cls, name, f):
    f.__name__ = '%s.%s' % (cls.__name__, name)
    setattr(cls, name, f)

def DefOperator(name, f):
    DefClsMethod(EUDVariable, name, f)

    def iop(self, rhs):
        self << f(self, rhs)
    DefClsMethod(EUDVariable, '__i%s' % name[2:], iop)

DefOperator('__mul__', f_mul)
DefOperator('__floordiv__', lambda x, y: f_div(x, y)[0])
DefOperator('__mod__', lambda x, y: f_div(x, y)[1])
DefOperator('__and__', f_bitand)
DefOperator('__or__', f_bitor)
DefOperator('__xor__', f_bitxor)
