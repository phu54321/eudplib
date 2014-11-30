from .. import core as c
from .basicstru import (
    EUDJump,
    EUDJumpIf,
    EUDJumpIfNot
)

_loopb_idset = set(['infloopblock', 'whileblock'])


def _IsLoopBlockId(idf):
    return idf in _loopb_idset


def EUDInfLoop():
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = block['loopstart']

    c.EUDCreateBlock('infloopblock', block)

    return True


def EUDEndInfLoop():
    lb = c.EUDPopBlock('infloopblock')
    assert lb[0] == 'infloopblock', 'Block start/end mismatch'
    EUDJump(lb[1]['loopstart'])
    lb[1]['loopend'] << c.NextTrigger()


# -------

def EUDWhile(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = block['loopstart']

    c.EUDCreateBlock('whileblock', block)

    EUDJumpIfNot(conditions, block['loopend'])

    return True


def EUDWhileNot(conditions):
    block = {
        'loopstart': c.NextTrigger(),
        'loopend': c.Forward(),
        'contpoint': None,
    }
    block['contpoint'] = block['loopstart']

    c.EUDCreateBlock('whileblock', block)

    EUDJumpIf(conditions, block['loopend'])

    return True


def EUDEndWhile():
    lb = c.EUDPopBlock('whileblock')
    EUDJump(lb[1]['loopstart'])
    lb[1]['loopend'] << c.NextTrigger()


# -------

def _GetLastLoopBlock():
    for block in reversed(c.EUDGetBlockList()):
        if block[0] in _loopb_idset:
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
    block['contpoint'] = c.NextTrigger()


def EUDLoopBreak():
    block = _GetLastLoopBlock()[1]
    EUDJump(block['loopend'])


def EUDLoopBreakIf(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIf(conditions, block['loopend'])


def EUDLoopBreakIfNot(conditions):
    block = _GetLastLoopBlock()[1]
    EUDJumpIfNot(conditions, block['loopend'])
