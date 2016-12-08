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

from eudplib import (
    core as c,
    ctrlstru as cs,
)


def EUDOr(cond1, *conds):
    """ cond1 || cond2 || ... || condn

    .. warning:: Short circuiting is not supported

    :param conds: List of conditions
    """

    v = c.EUDVariable()
    if cs.EUDIf()(cond1):
        v << 1
    for cond in conds:
        if cs.EUDElseIf()(cond):
            v << 1
    if cs.EUDElse()():
        v << 0
    cs.EUDEndIf()
    return v


def EUDAnd(cond1, *conds):
    """ cond1 && cond2 && ... && condn

    .. note::
        This function computes AND value of various conditions.
        If you don't want to do much computation, you should better use
        plain list instead of this function.

    .. warning:: Short circuiting is not supported.

    :param conds: List of conditions
    """

    v = c.EUDVariable()
    if cs.EUDIfNot()(cond1):
        v << 0
    for cond in conds:
        if cs.EUDElseIfNot()(cond):
            v << 0
    if cs.EUDElse()():
        v << 1
    cs.EUDEndIf()
    return v


def EUDNot(cond):
    """ !cond

    :param conds: Condition to negate
    """

    v = c.EUDVariable()
    if cs.EUDIf()(cond):
        v << 0
    if cs.EUDElse()():
        v << 1
    cs.EUDEndIf()
    return v
