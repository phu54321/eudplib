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
from eudplib import utils as ut
from .basicstru import (
    EUDJump,
    EUDJumpIf,
    EUDJumpIfNot
)

_loopb_idset = {'infloopblock', 'loopnblock', 'whileblock'}


def _IsLoopBlockId(idf):
    return idf in _loopb_idset


# -------


def EUDInfLoop():
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': c.Forward()
    }

    ut.EUDCreateBlock('infloopblock', block)

    return True


def EUDEndInfLoop():
    block = ut.EUDPopBlock('infloopblock')[1]
    if not block['contpoint'].IsSet():
        block['contpoint'] << block['loopstart']
    EUDJump(block['loopstart'])
    block['loopend'] << c.NextTrigger()


# -------


def EUDLoopN(n):
    vardb = c.Db(4)
    c.RawTrigger(actions=c.SetMemory(vardb, c.SetTo, n))

    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': c.Forward(),
        'vardb': vardb
    }

    ut.EUDCreateBlock('loopnblock', block)
    EUDJumpIf(c.Memory(vardb, c.Exactly, 0), block['loopend'])
    return True


def EUDEndLoopN():
    block = ut.EUDPopBlock('loopnblock')[1]
    if not block['contpoint'].IsSet():
        block['contpoint'] << c.NextTrigger()

    vardb = block['vardb']
    c.RawTrigger(actions=c.SetMemory(vardb, c.Subtract, 1))
    EUDJump(block['loopstart'])
    block['loopend'] << c.NextTrigger()


# -------


def EUDWhile(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': c.Forward(),
    }

    ut.EUDCreateBlock('whileblock', block)

    EUDJumpIfNot(conditions, block['loopend'])

    return True


def EUDWhileNot(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': c.Forward(),
    }

    ut.EUDCreateBlock('whileblock', block)

    EUDJumpIf(conditions, block['loopend'])

    return True


def EUDEndWhile():
    block = ut.EUDPopBlock('whileblock')[1]
    if not block['contpoint'].IsSet():
        block['contpoint'] << block['loopstart']
    EUDJump(block['loopstart'])
    block['loopend'] << c.NextTrigger()


# -------


def _GetLastLoopBlock():
    for block in reversed(ut.EUDGetBlockList()):
        if _IsLoopBlockId(block[0]):
            return block

    raise ut.EPError('No loop block surrounding this code area')


def EUDLoopContinue():
    block = _GetLastLoopBlock()[1]
    EUDJump(block['contpoint'])


def EUDLoopContinueIf(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIf(conditions, block['contpoint'])


def EUDLoopContinueIfNot(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIfNot(conditions, block['contpoint'])


def EUDLoopSetContinuePoint():
    block = _GetLastLoopBlock()[1]
    block['contpoint'] << c.NextTrigger()


def EUDLoopBreak():
    block = _GetLastLoopBlock()[1]
    EUDJump(block['loopend'])


def EUDLoopBreakIf(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIf(conditions, block['loopend'])


def EUDLoopBreakIfNot(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIfNot(conditions, block['loopend'])
