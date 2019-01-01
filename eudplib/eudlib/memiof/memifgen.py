#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2018 Armoha

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

from . import modcurpl as cp
from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)


def bits(n):
    n = n & 0xFFFFFFFF
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


def f_readgen_epd(mask, *args, docstring=None):
    @c.EUDFunc
    def f_read_epd_template(targetplayer):
        origcp = cp.f_getcurpl()
        ret = [c.EUDVariable() for _ in args]

        cs.DoActions([
            c.SetCurrentPlayer(targetplayer),
            [retv.SetNumber(arg[0]) for retv, arg in zip(ret, args)],
        ])

        for i in bits(mask):
            c.RawTrigger(
                conditions=[
                    c.DeathsX(c.CurrentPlayer, c.AtLeast, 1, 0, i)
                ],
                actions=[
                    retv.AddNumber(arg[1](i)) if arg[1](i) != 0 else []
                    for retv, arg in zip(ret, args)
                ],
            )

        cp.f_setcurpl(origcp)

        return ut.List2Assignable(ret)

    if docstring:
        f_read_epd_template.__doc__ = docstring

    return f_read_epd_template


def f_readgen_cp(mask, *args, docstring=None):
    @c.EUDFunc
    def readerf():
        ret = [c.EUDVariable() for _ in args]

        cs.DoActions([
            retv.SetNumber(arg[0]) for retv, arg in zip(ret, args)
        ])

        for i in bits(mask):
            c.RawTrigger(
                conditions=[
                    c.DeathsX(c.CurrentPlayer, c.AtLeast, 1, 0, i)
                ],
                actions=[
                    retv.AddNumber(arg[1](i)) if arg[1](i) != 0 else []
                    for retv, arg in zip(ret, args)
                ],
            )

        return ut.List2Assignable(ret)

    def f_read_cp_template(cpo):
        if not isinstance(cpo, int) or cpo != 0:
            cs.DoActions(c.SetMemory(0x6509B0, c.Add, cpo))
        ret = list(readerf())
        if not isinstance(cpo, int) or cpo != 0:
            cs.DoActions(c.SetMemory(0x6509B0, c.Add, -cpo))
        return ut.List2Assignable(ret)

    if docstring:
        f_read_cp_template.__doc__ = docstring

    return f_read_cp_template


f_cunitread_epd = f_readgen_epd(0x7FFFF8, (0, lambda x: x))
f_cunitread_cp = f_readgen_cp(0x7FFFF8, (0, lambda x: x))
f_cunitepdread_epd = f_readgen_epd(0x7FFFF8, (0, lambda x: x), (-0x58A364 // 4, lambda y: y // 4))
f_cunitepdread_cp = f_readgen_cp(0x7FFFF8, (0, lambda x: x), (-0x58A364 // 4, lambda y: y // 4))


def f_maskread_epd(targetplayer, mask, _fdict={}):
    if mask not in _fdict:
        _fdict[mask] = f_readgen_epd(mask, (0, lambda x: x))
    return _fdict[mask](targetplayer)


def f_maskread_cp(cpoffset, mask, _fdict={}):
    if mask not in _fdict:
        _fdict[mask] = f_readgen_cp(mask, (0, lambda x: x))
    return _fdict[mask](cpoffset)
