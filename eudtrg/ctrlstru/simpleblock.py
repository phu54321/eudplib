from .. import core as c
from .basicstru import EUDJump, EUDJumpIf, EUDJumpIfNot


'''
There are code duplication between EUDIf - EUDIfNot, EUDElseIf - EUDElseIfNot.
TODO : Remove code duplication if possible.
'''


def EUDIf(conditions):
    block = {
        'ifend': c.Forward(),
        'next_elseif': c.Forward()
    }
    c.EUDCreateBlock('ifblock', block)

    EUDJumpIfNot(conditions, block['next_elseif'])

    return True


def EUDIfNot(conditions):
    block = {
        'ifend': c.Forward(),
        'next_elseif': c.Forward()
    }
    c.EUDCreateBlock('ifblock', block)

    EUDJumpIf(conditions, block['next_elseif'])

    return True


# -------

def EUDElseIf(conditions):
    lb = c.EUDGetLastBlock()
    assert lb[0] == 'ifblock', 'Block start/end mismatch'
    block = lb[1]
    assert block['next_elseif'] is not None, (
        'Cannot have EUDElseIf after EUDElse')

    # Finish previous if/elseif block
    EUDJump(block['ifend'])

    block['next_elseif'] << c.NextTrigger()
    block['next_elseif'] = c.Forward()
    EUDJumpIfNot(conditions, block['next_elseif'])

    return True


def EUDElseIfNot(conditions):
    lb = c.EUDGetLastBlock()
    assert lb[0] == 'ifblock', 'Block start/end mismatch'
    block = lb[1]
    assert block['next_elseif'] is not None, (
        'Cannot have EUDElseIfNot after EUDElse')

    # Finish previous if/elseif block
    EUDJump(block['ifend'])
    block['next_elseif'] << c.NextTrigger()
    block['next_elseif'] = c.Forward()
    EUDJumpIf(conditions, block['next_elseif'])

    return True


# -------

def EUDElse():
    lb = c.EUDGetLastBlock()
    assert lb[0] == 'ifblock', 'Block start/end mismatch'
    block = lb[1]
    assert block['next_elseif'] is not None, (
        'Cannot have EUDElse after EUDElse')

    # Finish previous if/elseif block
    EUDJump(block['ifend'])
    block['next_elseif'] << c.NextTrigger()
    block['next_elseif'] = None

    return True


def EUDEndIf():
    lb = c.EUDPopBlock('ifblock')
    block = lb[1]

    # Finalize
    nei_fw = block['next_elseif']
    if nei_fw:
        nei_fw << c.NextTrigger()

    block['ifend'] << c.NextTrigger()


# -------

def EUDExecuteOnce():
    block = {
        'blockend': c.Forward()
    }
    c.EUDCreateBlock('executeonceblock')

    tv = c.Db(4)

    EUDJumpIf(c.Memory(tv, c.Exactly, 1), block['blockend'])
    c.Trigger(actions=c.SetMemory(tv, c.SetTo, 1))

    return True


def EUDEndExecuteOnce():
    lb = c.EUDPopBlock('executeonceblock')
    assert lb[0] == 'executeonceblock', 'Block start/end mismatch'
    block = lb[1]

    block['blockend'] << c.NextTrigger()
