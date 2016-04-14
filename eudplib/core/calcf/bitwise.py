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

from .. import varfunc as vf
from .. import rawtrigger as rt
from .muldiv import f_mul, f_div


def bw_gen(cond, docstring=None):
    @vf.EUDFunc
    def f_bitsize_template(a, b):
        tmp = vf.EUDLightVariable()
        ret = vf.EUDVariable()

        ret << 0

        for i in range(31, -1, -1):
            rt.RawTrigger(
                conditions=[
                    a.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    a.SubtractNumber(2 ** i)
                ]
            )

            rt.RawTrigger(
                conditions=[
                    b.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    b.SubtractNumber(2 ** i)
                ]
            )

            rt.RawTrigger(
                conditions=cond(tmp),
                actions=ret.AddNumber(2 ** i)
            )

            tmp << 0

        return ret

    if docstring:
        f_bitsize_template.__doc__ = docstring

    return f_bitsize_template


f_bitand = bw_gen(lambda x: x.Exactly(2), "Calculate a & b")
f_bitor = bw_gen(lambda x: x.AtLeast(1), "Calculate a | b")
f_bitxor = bw_gen(lambda x: x.Exactly(1), "Calculate a ^ b")
f_bitnand = bw_gen(lambda x: x.Exactly(0), "Calculate ~(a & b)")
f_bitnor = bw_gen(lambda x: x.AtMost(1), "Calculate ~(a | b)")


def f_bitnxor(a, b):
    """Calculate ~(a ^ b)"""
    return f_bitnot(f_bitxor(a, b))


def f_bitnot(a):
    """Calculate ~a"""
    return 0xFFFFFFFF - a


# -------


@vf.EUDFunc
def f_bitsplit(a):
    """Splits bit of given number

    :returns: int bits[32];  // bits[i] = (ith bit from LSB of a is set)
    """
    bits = vf.EUDCreateVariables(32)
    for i in range(31, -1, -1):
        bits[i] << 0
        rt.RawTrigger(
            conditions=a.AtLeast(2 ** i),
            actions=[
                a.SubtractNumber(2 ** i),
                bits[i].SetNumber(1)
            ]
        )
    return bits


# -------

@vf.EUDFunc
def _exp2_vv(n):
    ret = vf.EUDVariable()
    for i in range(32):
        rt.RawTrigger(
            conditions=[n == i],
            actions=[ret.SetNumber((2 ** i))]
        )
    return ret


def _exp2(n):
    if isinstance(n, int):
        return 1 << n

    else:
        return _exp2_vv(n)


def f_bitlshift(a, b):
    """a << b"""
    return f_mul(a, _exp2(b))


def f_bitrshift(a, b):
    """Calculate a >> b"""
    if isinstance(b, int) and b >= 32:
        return 0

    ret = vf.EUDVariable()
    ret << f_div(a, _exp2(b))
    return ret
