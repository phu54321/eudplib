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
from .basicstru import EUDJump, EUDBranch


def _IsSwitchBlockId(idf):
    return idf == 'swblock'


def EUDSwitch(var):
    block = {
        'targetvar': var,
        'casebrlist': {},
        'defaultbr': c.Forward(),
        'swend': c.Forward()
    }

    c.PushTriggerScope()
    c.EUDCreateBlock('swblock', block)

    return True


def EUDSwitchCase(begin, end=None):
    assert isinstance(begin, int) or isinstance(begin, c.SCMemAddr), (
        'Invalid selector start for EUDSwitch')
    if end is None:
        end = begin + 1
    assert isinstance(begin, int) or isinstance(begin, c.SCMemAddr), (
        'Invalid selector end for EUDSwitch')

    lb = c.EUDGetLastBlock()
    assert lb[0] == 'swblock', 'Block start/end mismatch'
    block = lb[1]

    assert number not in block['casebrlist'], 'Duplicate cases'
    block['casebrlist'][number] = c.NextTrigger()


def EUDSwitchDefault():
    lb = c.EUDGetLastBlock()
    assert lb[0] == 'swblock', 'Block start/end mismatch'
    block = lb[1]

    assert not block['defaultbr'].IsSet(), 'Duplicate default'
    block['defaultbr'] << c.NextTrigger()


def EUDSwitchBreak():
    block = c.EUDGetLastBlockOfName('swblock')[1]
    EUDJump(block['swend'])


def EUDEndSwitch():
    lb = c.EUDPopBlock('swblock')
    block = lb[1]
    swend = block['swend']
    EUDJump(swend)  # Exit switch block
    c.PopTriggerScope()

    # If default block is not specified, skip it
    if not block['defaultbr'].IsSet():
        block['defaultbr'] << swend

    # Create key selector
    casebrlist = block['casebrlist']
    defbranch = block['defaultbr']
    casekeylist = sorted(block['casebrlist'].keys())
    var = block['targetvar']

    def KeySelector(keys):
        # Uses simple binary search
        ret = c.NextTrigger()
        if len(keys) == 1:  # Only one keys on the list
            EUDBranch(var == keys[0], casebrlist[keys[0]], defbranch)

        elif len(keys) >= 2:
            br1 = c.Forward()
            br2 = c.Forward()
            midpos = len(keys) // 2
            midval = keys[midpos]

            EUDBranch(var <= midval, br1, br2)
            br1 << KeySelector(keys[:midpos + 1])
            br2 << KeySelector(keys[midpos + 1:])

        else:  # len(keys) == 0
            EUDJump(defbranch)

        return ret

    KeySelector(casekeylist)

    swend << c.NextTrigger()
