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

from ..mapdata import (
    GetLocationIndex,
    GetStringIndex,
    GetSwitchIndex,
    GetUnitIndex
)

from ...utils import u2b, b2i4

from .strdict import (
    DefAIScriptDict,
    DefLocationDict,
    DefSwitchDict,
    DefUnitDict
)


def EncodeAIScript(ais):
    if type(ais) is str:
        ais = u2b(ais)

    if type(ais) is bytes:
        assert len(ais) >= 4, 'AIScript name too short'

        if len(ais) > 4:
            return b2i4(DefAIScriptDict[ais])

        elif len(ais) == 4:
            return b2i4(ais)

    else:
        return ais


def _EncodeAny(f, dl, s):
    try:
        return f(s)

    except:
        try:
            return dl.get(s, s)

        except TypeError:  # unhashable
            return s


def EncodeLocation(loc):
    return _EncodeAny(lambda s: GetLocationIndex(s) + 1, DefLocationDict, loc)


def EncodeString(s):
    return _EncodeAny(GetStringIndex, {}, s)


def EncodeSwitch(sw):
    return _EncodeAny(GetSwitchIndex, DefSwitchDict, sw)


def EncodeUnit(u):
    return _EncodeAny(GetUnitIndex, DefUnitDict, u)
