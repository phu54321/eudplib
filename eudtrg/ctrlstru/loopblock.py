#!/usr/bin/python
#-*- coding: utf-8 -*-

from .. import core as c
from .basicstru import (
    EUDJump,
    EUDJumpIf,
    EUDJumpIfNot
)

_loopb_idset = set(['infloopblock', 'whileblock'])


def _IsLoopBlockId(idf):
    return idf in _loopb_idset


# -------


def EUDInfLoop():
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = c.Forward()

    c.EUDCreateBlock('infloopblock', block)

    return True


def EUDEndInfLoop():
    block = c.EUDPopBlock('infloopblock')[1]
    if not block['contpoint'].IsSet():
        block['contpoint'] << block['loopstart']
    EUDJump(block['loopstart'])
    block['loopend'] << c.NextTrigger()


# -------


def EUDWhile(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = c.Forward()

    c.EUDCreateBlock('whileblock', block)

    EUDJumpIfNot(conditions, block['loopend'])

    return True


def EUDWhileNot(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = c.Forward()

    c.EUDCreateBlock('whileblock', block)

    EUDJumpIf(conditions, block['loopend'])

    return True


def EUDEndWhile():
    block = c.EUDPopBlock('whileblock')[1]
    if not block['contpoint'].IsSet():
        block['contpoint'] << block['loopstart']
    EUDJump(block['loopstart'])
    block['loopend'] << c.NextTrigger()


# -------


def _GetLastLoopBlock():
    for block in reversed(c.EUDGetBlockList()):
        if _IsLoopBlockId(block[0]):
            return block

    raise AssertionError('No loop block surrounding this code area')


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
