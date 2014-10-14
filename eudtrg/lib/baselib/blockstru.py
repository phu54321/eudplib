import eudtrg.base as b

from . import ctrlstru as cs


_blocktokens = []


'''
If ~ Elseif ~ Else ~ EndIf structure
'''


def EUDIf(conditions):
    """Create if block for eudtrg program.

    :param conditions: Conditions to execute following blocks.
    :returns: True
    """
    if_end = b.Forward()
    next_elseif = b.Forward()
    if_token = ['if', if_end, next_elseif]
    _blocktokens.append(if_token)

    cs.EUDJumpIfNot(conditions, next_elseif)

    # Enter if block

    return True  # Support syntax like '    if EUDIf(..):  ~~ EUDEndIf()'


def EUDIfNot(conditions):
    """Create if block for eudtrg program.

    :param conditions: Conditions to execute following blocks.
    :returns: True
    """
    if_end = b.Forward()
    next_elseif = b.Forward()
    if_token = ['if', if_end, next_elseif]
    _blocktokens.append(if_token)

    cs.EUDJumpIf(conditions, next_elseif)

    # Enter if block

    return True  # Support syntax like '    if EUDIf(..):  ~~ EUDEndIf()'


def EUDElseIf(conditions):
    """Create elif block for eudtrg program.

    :param conditions: Conditions to execute following blocks.
    :returns: True
    """
    iftoken = _blocktokens[-1]
    assert iftoken[0] == 'if', (
        "Block token mismatch : expected 'if', got '%s'" % iftoken[0])
    if_end = iftoken[1]
    next_elseif = iftoken[2]

    cs.EUDJump(if_end)
    # Out of former if block

    # Enter else-if block
    next_elseif << b.NextTrigger()
    next_elseif = b.Forward()
    iftoken[2] = next_elseif
    cs.EUDJumpIfNot(conditions, next_elseif)

    return True


def EUDElseIfNot(conditions):
    """Create elif block for eudtrg program.

    :param conditions: Conditions to execute following blocks.
    :returns: True
    """
    iftoken = _blocktokens[-1]
    assert iftoken[0] == 'if', (
        "Block token mismatch : expected 'if', got '%s'" % iftoken[0])
    if_end = iftoken[1]
    next_elseif = iftoken[2]

    cs.EUDJump(if_end)
    # Out of former if block

    # Enter else-if block
    next_elseif << b.NextTrigger()
    next_elseif = b.Forward()
    iftoken[2] = next_elseif
    cs.EUDJumpIf(conditions, next_elseif)

    return True


def EUDElse():
    """Create else block for eudtrg program.

    :returns: True
    """
    iftoken = _blocktokens[-1]
    assert iftoken[0] == 'if', (
        "Block token mismatch : expected 'if', got '%s'" % iftoken[0])
    if_end = iftoken[1]
    next_elseif = iftoken[2]

    cs.EUDJump(if_end)
    # Out of former if block

    # Enter else-if block
    next_elseif << b.NextTrigger()
    iftoken[2] = None

    return True


def EUDEndIf():
    """End if~elif~endif block for eudtrg program."""

    iftoken = _blocktokens[-1]
    assert iftoken[0] == 'if', (
        "Block token mismatch : expected 'if', got '%s'" % iftoken[0])
    if_end = iftoken[1]
    next_elseif = iftoken[2]

    if next_elseif:
        next_elseif << b.NextTrigger()

    # Out of former if block
    if_end << b.NextTrigger()
    _blocktokens.pop()


'''
While ~ EndWhile structure
'''


def EUDWhile(conditions):
    while_start = b.Forward()
    while_end = b.Forward()
    while_contstart = b.Forward()
    whiletoken = ['while', while_start, while_end, while_contstart]
    _blocktokens.append(whiletoken)

    while_start << b.NextTrigger()
    cs.EUDJumpIfNot(conditions, while_end)

    return True


def EUDWhileNot(conditions):
    while_start = b.Forward()
    while_end = b.Forward()
    while_contstart = b.Forward()
    whiletoken = ['while', while_start, while_end, while_contstart]
    _blocktokens.append(whiletoken)

    while_start << b.NextTrigger()
    cs.EUDJumpIf(conditions, while_end)

    return True


def EUDEndWhile():
    whiletoken = _blocktokens[-1]
    assert whiletoken[0] == 'while', (
        "Block token mismatch : expected 'while', got '%s'" % whiletoken[0])

    while_start = whiletoken[1]
    while_end = whiletoken[2]
    while_contstart = whiletoken[3]

    if while_contstart.ForwardEmpty():
        while_contstart << while_start

    cs.EUDJump(while_start)
    while_end << b.NextTrigger()
    _blocktokens.pop()


'''
DoWhile ~ EndDowhile structure
'''


def EUDDoWhile():
    dowhile_start = b.Forward()
    dowhile_end = b.Forward()
    dowhile_contstart = b.Forward()
    dowhiletoken = ['dowhile', dowhile_start, dowhile_end, dowhile_contstart]
    _blocktokens.append(dowhiletoken)

    dowhile_start << b.NextTrigger()

    return True


def EUDEndDoWhile(conditions):
    dowhiletoken = _blocktokens[-1]
    assert dowhiletoken[0] == 'dowhile', (
        "Block token mismatch : expected 'dowhile', got '%s'"
        % dowhiletoken[0])

    dowhile_start = dowhiletoken[1]
    dowhile_end = dowhiletoken[2]
    dowhile_contstart = dowhiletoken[3]

    if dowhile_contstart.ForwardEmpty():
        dowhile_contstart << dowhile_start

    cs.EUDJumpIf(conditions, dowhile_start)

    dowhile_end << b.NextTrigger()
    _blocktokens.pop()


'''
ExecuteOnce ~ EndExecuteOnce structure
'''


def EUDExecuteOnce():
    execute_start = b.Forward()
    execute_end = b.Forward()
    execonce_token = ['execonce', execute_start, execute_end]
    _blocktokens.append(execonce_token)

    execute_start << b.Trigger()

    return True


def EUDEndExecuteOnce():
    execonce_token = _blocktokens[-1]
    assert execonce_token[0] == 'execonce', (
        "Block token mismatch : expected 'execonce', got '%s'"
        % execonce_token[0])

    execute_start = execonce_token[1]
    execute_end = execonce_token[2]

    cs.DoActions(b.SetNextPtr(execute_start, execute_end))
    execute_end << b.NextTrigger()
    _blocktokens.pop()


'''
Break, Continue support for loops
'''


def _IsLoopToken(token):
    return token[0] in ['dowhile', 'while']


def _GetLoopToken():
    for token in reversed(_blocktokens):
        if _IsLoopToken(token):
            return token

    raise RuntimeError('Cannot find outer loop')


def EUDSetContinuePoint():
    _GetLoopToken()[3] << b.NextTrigger()


def EUDContinue():
    continue_start = _GetLoopToken()[3]
    cs.EUDJump(continue_start)


def EUDContinueIf(conditions):
    continue_start = _GetLoopToken()[3]
    cs.EUDJumpIf(conditions, continue_start)


def EUDContinueIfNot(conditions):
    continue_start = _GetLoopToken()[3]
    cs.EUDJumpIfNot(conditions, continue_start)


def EUDBreak():
    loopend = _GetLoopToken()[2]
    cs.EUDJump(loopend)


def EUDBreakIf(conditions):
    loopend = _GetLoopToken()[2]
    cs.EUDJumpIf(conditions, loopend)


def EUDBreakIfNot(conditions):
    loopend = _GetLoopToken()[2]
    cs.EUDJumpIfNot(conditions, loopend)
