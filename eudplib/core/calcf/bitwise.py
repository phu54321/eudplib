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

from eudplib import core as c
from eudplib import ctrlstru as cs
from eudplib.core.calcf.muldiv import f_mul, f_div


def bw_gen(cond):
    @c.EUDFunc
    def f_bitsize_template(a, b):
        tmp = c.EUDLightVariable()
        ret = c.EUDVariable()

        ret << 0

        for i in range(31, -1, -1):
            c.RawTrigger(
                conditions=[
                    a.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    a.SubtractNumber(2 ** i)
                ]
            )

            c.RawTrigger(
                conditions=[
                    b.AtLeast(2 ** i)
                ],
                actions=[
                    tmp.AddNumber(1),
                    b.SubtractNumber(2 ** i)
                ]
            )

            c.RawTrigger(
                conditions=cond(tmp),
                actions=ret.AddNumber(2 ** i)
            )

            cs.DoActions(tmp.SetNumber(0))

        return ret

    return f_bitsize_template


f_bitand = bw_gen(lambda x: x.Exactly(2))
f_bitor = bw_gen(lambda x: x.AtLeast(1))
f_bitxor = bw_gen(lambda x: x.Exactly(1))

f_bitnand = bw_gen(lambda x: x.Exactly(0))
f_bitnor = bw_gen(lambda x: x.AtMost(1))


@c.EUDFunc
def f_bitnxor(a, b):
    return f_bitnot(f_bitxor(a, b))


def f_bitnot(a):
    return 0xFFFFFFFF - a


# -------


@c.EUDFunc
def f_bitsplit(a):
    bits = [c.EUDCreateVariables(32)]
    for i in range(31, -1, -1):
        cs.DoActions(bits[i].SetNumber(0))
        c.RawTrigger(
            conditions=a.AtLeast(2 ** i),
            actions=[
                a.SubtractNumber(2 ** i),
                bits[i].SetNumber(1)
            ]
        )
    return bits


# -------

@c.EUDFunc
def _exp2_vv(n):
    ret = c.EUDVariable()
    cs.EUDSwitch(n)
    for i in range(32):
        cs.EUDSwitchCase(i)
        ret << 1 ** i
    cs.EUDSwitchDefault()
    ret << 0  # overflow
    cs.EUDEndSwitch()
    return ret


def _exp2(n):
    if isinstance(n, int):
        return 1 << n

    else:
        return _exp2_vv(n)


def f_bitlshift(a, b):
    return f_mul(a, _exp2(b))


def f_bitrshift(a, b):
    if isinstance(b, int) and b >= 32:
        return 0

    ret = c.EUDVariable()
    if cs.EUDIf(b >= 32):
        ret << 0
    if cs.EUDElse():
        ret << f_div(a, _exp2(b))
    return ret
