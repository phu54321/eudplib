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

from .. import core as c


def DoActions(actions):
    return c.Trigger(actions=c.FlattenList(actions))


def EUDJump(nextptr):
    return c.Trigger(nextptr=nextptr)


def EUDBranch(conditions, ontrue, onfalse):
    brtrg = c.Forward()
    ontruetrg = c.Forward()

    brtrg << c.Trigger(
        nextptr=onfalse,
        conditions=conditions,
        actions=[
            c.SetNextPtr(brtrg, ontruetrg)
        ]
    )

    ontruetrg << c.Trigger(
        nextptr=ontrue,
        actions=[
            c.SetNextPtr(brtrg, onfalse)
        ]
    )


def EUDJumpIf(conditions, ontrue):
    onfalse = c.Forward()
    EUDBranch(conditions, ontrue, onfalse)
    onfalse << c.NextTrigger()


def EUDJumpIfNot(conditions, onfalse):
    ontrue = c.Forward()
    EUDBranch(conditions, ontrue, onfalse)
    ontrue << c.NextTrigger()
