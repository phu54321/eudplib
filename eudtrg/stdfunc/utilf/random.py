# This code uses LCG with constants defined from ANSI C
# See http://en.wikipedia.org/wiki/Linear_congruential_generator

from ... import core as c
from ... import varfunc as vf
from ..memiof import f_dwbreak
from ..calcf import f_mul

_seed = vf.EUDVariable()


@vf.EUDFunc
def getseed():
    return _seed


@vf.EUDFunc
def srand(seed):
    _seed << seed


@vf.EUDFunc
def rand():
    _seed << f_mul(_seed, 1103515245) + 12345
    return f_dwbreak(_seed)[1]  # Only HIWORD is returned


@vf.EUDFunc
def dwrand():
    seed1 = f_mul(_seed, 1103515245) + 12345
    seed2 = f_mul(seed1, 1103515245) + 12345
    _seed << seed2

    ret = vf.EUDVariable()
    ret << 0

    # HIWORD
    for i in range(31, 15, -1):
        c.Trigger(
            conditions=seed1.AtLeast(2 ** i),
            actions=[
                seed1.SubtractNumber(2 ** i),
                ret.AddNumber(2 ** i),
            ]
        )

    # LOWORD
    for i in range(31, 15, -1):
        c.Trigger(
            conditions=seed2.AtLeast(2 ** i),
            actions=[
                seed2.SubtractNumber(2 ** i),
                ret.AddNumber(2 ** (i - 16)),
            ]
        )

    return ret
