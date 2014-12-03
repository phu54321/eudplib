#!/usr/bin/python
#-*- coding: utf-8 -*-

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


def EUDSwitchCase(number):
    assert isinstance(number, int) or isinstance(number, c.SCMemAddr), (
        'Invalid selector for EUDSwitch')

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
            br1 = KeySelector(keys[:midpos+1])
            br2 = KeySelector(keys[midpos+1:])

        else:  # len(keys) == 0
            EUDJump(defbranch)

        return ret

    KeySelector(casekeylist)

    swend << c.NextTrigger()
