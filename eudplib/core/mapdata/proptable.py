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

'''
Unit property table manager.
'''

from .unitprp import UnitProperty

_uprpdict = {}
_uprptable = []


def InitPropertyMap(chkt):
    global _prptable, _uprpdict
    _uprpdict.clear()
    _uprptable.clear()


def GetPropertyIndex(prop):
    assert isinstance(prop, UnitProperty)

    prop = bytes(prop)
    try:
        return _uprpdict[prop] + 1  # SC counts unit properties from 1. Sucks

    except KeyError:
        uprpindex = len(_uprptable)
        assert uprpindex < 64, 'Unit property table overflow'

        _uprptable.append(prop)
        _uprpdict[prop] = uprpindex
        return uprpindex + 1  # SC counts unit properties from 1. Sucks


def ApplyPropertyMap(chkt):
    uprpdata = b''.join(_uprptable) + bytes(20 * (64 - len(_uprptable)))
    chkt.setsection('UPRP', uprpdata)
