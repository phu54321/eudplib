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

# This code xorshift algorithm at http://www.jstatsoft.org/v08/i14/paper
#
# unsigned long xor() {
# static unsigned long y=2463534242;
#     yˆ=(y<<13);
#     y=(y>>17);
#     return (yˆ=(y<<5));
# }
#

from ... import core as c
from ... import varfunc as vf
from ..memiof import f_dwbreak, f_dwread_epd
from ..calcf import f_bitxor, f_mul

_seed = vf.EUDVariable()


def f_getseed():
    t = vf.EUDVariable()
    t << _seed
    return t


def f_srand(seed):
    _seed << seed


def f_randomize():
    current_rv = f_dwread_epd(c.EPD(0x51CA14))
    c.Trigger(
        conditions=current_rv.Exactly(0),
        actions=current_rv.SetNumber(30)
    )
    _seed << current_rv


@vf.EUDFunc
def f_rand():
    _seed << f_mul(_seed, 1103515245) + 12345
    return f_dwbreak(_seed)[1]  # Only HIWORD is returned


@vf.EUDFunc
def f_dwrand():
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
