#!/usr/bin/python
#-*- coding: utf-8 -*-

from .import (
    loopblock as lb,
    swblock as sb
)

from .. import core as c


def EUDContinue():
    return lb.EUDLoopContinue()


def EUDContinueIf(conditions):
    return lb.EUDLoopContinueIf(conditions)


def EUDContinueIfNot(conditions):
    return lb.EUDLoopContinueIfNot(conditions)


def EUDSetContinuePoint():
    return lb.EUDLoopSetContinuePoint()


# -------


def EUDBreak():
    for block in reversed(c.EUDGetBlockList()):
        if lb._IsLoopBlockId(block[0]):
            lb.EUDLoopBreak()
            return
        elif sb._IsSwitchBlockId(block[0]):
            sb.EUDSwitchBreak()
            return

    raise AssertionError('No loop/switch block surrounding this code area')


def EUDBreakIf(conditions):
    for block in reversed(c.EUDGetBlockList()):
        if lb._IsLoopBlockId(block[0]):
            lb.EUDLoopBreakIf(conditions)
            return
        elif sb._IsSwitchBlockId(block[0]):
            sb.EUDSwitchBreakIf(conditions)
            return

    raise AssertionError('No loop/switch block surrounding this code area')


def EUDBreakIfNot(conditions):
    for block in reversed(c.EUDGetBlockList()):
        if lb._IsLoopBlockId(block[0]):
            lb.EUDLoopBreakIfNot(conditions)
            return
        elif sb._IsSwitchBlockId(block[0]):
            sb.EUDSwitchBreakIfNot(conditions)
            return

    raise AssertionError('No loop/switch block surrounding this code area')
