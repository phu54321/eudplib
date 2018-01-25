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

from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

from .modcurpl import (
    f_setcurpl,
    f_getcurpl,
)


@c.EUDFunc
def f_dwepdread_epd(targetplayer):
    origcp = f_getcurpl()
    ptr, epd = c.EUDVariable(), c.EUDVariable()
    cs.DoActions([
        ptr.SetNumber(0),
        epd.SetNumber(ut.EPD(0)),
        c.SetCurrentPlayer(targetplayer)
    ])

    for i in range(31, -1, -1):
        c.RawTrigger(
            conditions=[
                c.Deaths(c.CurrentPlayer, c.AtLeast, 2**i, 0)
            ],
            actions=[
                c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**i, 0),
                ptr.AddNumber(2 ** i),
                epd.AddNumber(2 ** (i - 2)) if i >= 2 else []
            ]
        )

    cs.DoActions(c.SetDeaths(c.CurrentPlayer, c.SetTo, ptr, 0))
    f_setcurpl(origcp)

    return ptr, epd


@c.EUDFunc
def f_dwread_epd(targetplayer):
    origcp = f_getcurpl()
    ptr = c.EUDVariable()
    cs.DoActions([
        ptr.SetNumber(0),
        c.SetCurrentPlayer(targetplayer)
    ])
    for i in range(31, -1, -1):
        c.RawTrigger(
            conditions=[
                c.Deaths(c.CurrentPlayer, c.AtLeast, 2**i, 0)
            ],
            actions=[
                c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**i, 0),
                ptr.AddNumber(2 ** i),
            ]
        )

    cs.DoActions([
        c.SetDeaths(c.CurrentPlayer, c.SetTo, ptr, 0),
        c.SetCurrentPlayer(origcp),
    ])

    return ptr


def f_epdread_epd(targetplayer):
    return f_dwepdread_epd(targetplayer)[1]


# Special flag reading functions
def f_flagread_epd(targetplayer, *flags, _readerdict={}):
    flags = tuple(flags)    # Make flags hashable

    if flags in _readerdict:
        readerf = _readerdict[flags]
    else:
        # Create reader function
        @c.EUDFunc
        def readerf(targetplayer):
            origcp = f_getcurpl()
            f_setcurpl(targetplayer)

            resetteract = c.Forward()
            flagsv = [c.EUDVariable() for _ in range(len(flags))]

            # All set to 0
            c.RawTrigger(
                actions=[
                    c.SetMemory(resetteract + 20, c.SetTo, 0),
                    [flagv.SetNumber(0) for flagv in flagsv]
                ]
            )

            # Fill flags
            for i in range(31, -1, -1):
                c.RawTrigger(
                    conditions=[
                        c.Deaths(c.CurrentPlayer, c.AtLeast, 2**i, 0)
                    ],
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**i, 0),
                        c.SetMemory(resetteract + 20, c.Add, 2 ** i),
                        [
                            flagv.AddNumber(2 ** i)
                            for j, flagv in enumerate(flagsv)
                            if flags[j] & (2 ** i)
                        ]
                    ]
                )

            c.RawTrigger(actions=[
                resetteract << c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0)
            ])
            f_setcurpl(origcp)

            return flagsv

        _readerdict[flags] = readerf

    return readerf(targetplayer)


# Writing functions

def f_dwwrite_epd(targetplayer, value):
    cs.DoActions(c.SetDeaths(targetplayer, c.SetTo, value, 0))


def f_dwadd_epd(targetplayer, value):
    cs.DoActions(c.SetDeaths(targetplayer, c.Add, value, 0))


def f_dwsubtract_epd(targetplayer, value):
    cs.DoActions(c.SetDeaths(targetplayer, c.Subtract, value, 0))


# Dword breaking functions
@c.EUDFunc
def f_dwbreak(number):
    """Get hiword/loword/4byte of dword"""
    word = c.EUDCreateVariables(2)
    byte = c.EUDCreateVariables(4)

    # Clear byte[], word[]
    cs.DoActions([
        word[0].SetNumber(0),
        word[1].SetNumber(0),
        byte[0].SetNumber(0),
        byte[1].SetNumber(0),
        byte[2].SetNumber(0),
        byte[3].SetNumber(0)
    ])

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16
        byteexp = i % 8
        wordexp = i % 16

        c.RawTrigger(
            conditions=number.AtLeast(2 ** i),
            actions=[
                byte[byteidx].AddNumber(2 ** byteexp),
                word[wordidx].AddNumber(2 ** wordexp),
                number.SubtractNumber(2 ** i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]


@c.EUDFunc
def f_dwbreak2(number):
    """Get hiword/loword/4byte of dword"""
    word = c.EUDCreateVariables(2)
    byte = c.EUDCreateVariables(4)

    # Clear byte[], word[]
    cs.DoActions([
        word[0].SetNumber(0),
        word[1].SetNumber(0),
        byte[0].SetNumber(0),
        byte[1].SetNumber(0),
        byte[2].SetNumber(0),
        byte[3].SetNumber(0)
    ])

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16

        c.RawTrigger(
            conditions=number.AtLeast(2 ** i),
            actions=[
                byte[byteidx].AddNumber(2 ** i),
                word[wordidx].AddNumber(2 ** i),
                number.SubtractNumber(2 ** i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]
