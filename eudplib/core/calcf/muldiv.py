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


def f_mul(a, b):
    if isinstance(a, c.EUDVariable) and isinstance(b, c.EUDVariable):
        return _f_mul(a, b)

    elif isinstance(a, c.EUDVariable):
        return f_constmul(b)(a)

    elif isinstance(b, c.EUDVariable):
        return f_constmul(a)(b)

    else:
        ret = c.EUDVariable()
        ret << a * b
        return ret


def f_div(a, b):
    """ returns (a//b, a%b) """
    if isinstance(b, c.EUDVariable):
        return _f_div(a, b)

    elif isinstance(a, c.EUDVariable):
        return f_constdiv(b)(a)

    else:
        if b:
            q, m = a // b, a % b
        else:
            q, m = 0xFFFFFFFF, a
        vq, vm = c.EUDCreateVariables(2)
        c.SeqCompute([
            (vq, c.SetTo, q),
            (vm, c.SetTo, vm)
        ])
        return vq, vm


# -------


def f_constmul(number):
    if not hasattr(f_constmul, 'mulfdict'):
        f_constmul.mulfdict = {}

    mulfdict = f_constmul.mulfdict

    try:
        return mulfdict[number]
    except KeyError:
        @c.EUDFunc
        def mulf(a):
            ret = c.EUDVariable()
            ret << 0
            for i in range(31, -1, -1):
                c.RawTrigger(
                    conditions=a.AtLeast(2 ** i),
                    actions=[
                        a.SubtractNumber(2 ** i),
                        ret.AddNumber(2 ** i * number)
                    ]
                )
            return ret

        mulfdict[number] = mulf
        return mulf


def f_constdiv(number):
    if not hasattr(f_constdiv, 'divfdict'):
        f_constdiv.divfdict = {}

    divfdict = f_constdiv.divfdict

    try:
        return divfdict[number]
    except KeyError:
        @c.EUDFunc
        def divf(a):
            ret = c.EUDVariable()
            ret << 0
            for i in range(31, -1, -1):
                # number too big
                if 2 ** i * number >= 2 ** 32:
                    continue

                c.RawTrigger(
                    conditions=a.AtLeast(2 ** i * number),
                    actions=[
                        a.SubtractNumber(2 ** i * number),
                        ret.AddNumber(2 ** i)
                    ]
                )
            return ret, a

        divfdict[number] = divf
        return divf


# -------


@c.EUDFunc
def _f_mul(a, b):
    ret, y0 = c.EUDCreateVariables(2)

    # Init
    c.SeqCompute([
        (ret, c.SetTo, 0),
        (y0, c.SetTo, b)
    ])

    chain = [c.Forward() for _ in range(32)]
    chain_y0 = [c.Forward() for _ in range(32)]

    # Calculate chain_y0
    for i in range(32):
        c.SeqCompute((
            (c.EPD(chain_y0[i]), c.SetTo, y0),
            (y0, c.Add, y0)
        ))
        if i <= 30:
            cs.EUDJumpIf(a.AtMost(2 ** (i + 1) - 1), chain[i])

    # Run multiplication chain
    for i in range(31, -1, -1):
        cy0 = c.Forward()

        chain[i] << c.RawTrigger(
            conditions=[
                a.AtLeast(2 ** i)
            ],
            actions=[
                a.SubtractNumber(2 ** i),
                cy0 << ret.AddNumber(0)
            ]
        )

        chain_y0[i] << cy0 + 20

    return ret


@c.EUDFunc
def _f_div(a, b):
    ret, x = c.EUDCreateVariables(2)

    # Init
    c.SeqCompute([
        (ret, c.SetTo, 0),
        (x, c.SetTo, b),
    ])

    # Chain c.forward decl
    chain_x0 = [c.Forward() for _ in range(32)]
    chain_x1 = [c.Forward() for _ in range(32)]
    chain = [c.Forward() for _ in range(32)]

    # Fill in chain
    for i in range(32):
        c.SeqCompute([
            (c.EPD(chain_x0[i]), c.SetTo, x),
            (c.EPD(chain_x1[i]), c.SetTo, x),
        ])

        cs.EUDJumpIf(x.AtLeast(0x8000000), chain[i])

        c.SeqCompute([
            (x, c.Add, x),
        ])

    # Run division chain
    for i in range(31, -1, -1):
        cx0, cx1 = c.Forward(), c.Forward()
        chain[i] << c.RawTrigger(
            conditions=[
                cx0 << a.AtLeast(0)
            ],
            actions=[
                cx1 << a.SubtractNumber(0),
                ret.AddNumber(2 ** i)
            ]
        )

        chain_x0[i] << cx0 + 8
        chain_x1[i] << cx1 + 20

    return ret, a  # a : remainder
