from eudtrg import LICENSE  # @UnusedImport

from eudtrg.base import *  # @UnusedWildImport


def DoActions(actions):
    '''
    Shortcut for creating trigger with only action fields specified.

    :param actions: Trigger actions.
    '''
    return Trigger(actions=FlattenList(actions))


def EUDJump(nextptr):
    '''
    Trigger with only nextptr specified. Useful for controlling trigger
    execution order. Acts as jmp instruction of x86 assembly.

    :param nextptr: Trigger to execute next.
    '''
    return Trigger(nextptr=nextptr)


def EUDBranch(conditions, ontrue, onfalse):
    '''
    Branch based on conditions.

    :param conditions: Conditions to check.
    :param ontrue: Trigger to execute when conditions are met.
    :param onfasle: Trigger to execute when conditions are not met.
    '''
    brtrg = Forward()
    ontruetrg = Forward()

    brtrg << Trigger(
        nextptr=onfalse,
        conditions=conditions,
        actions=[
            SetNextPtr(brtrg, ontruetrg)
        ]
    )

    ontruetrg << Trigger(
        nextptr=ontrue,
        actions=[
            SetNextPtr(brtrg, onfalse)
        ]
    )


def EUDJumpIf(conditions, ontrue):
    '''
    Jump if conditions are met. Two triggers are executed when jumping. If jump
    conditions are not met, then the following triggers are executed.

    :param conditions: Jump condition.
    :param ontrue: Trigger to execute when conditions are met.
    '''

    brtrg = Forward()
    ontruetrg = Forward()
    onfalse = Forward()

    brtrg << Trigger(
        nextptr=onfalse,
        conditions=conditions,
        actions=[
            SetNextPtr(brtrg, ontruetrg)
        ]
    )

    ontruetrg << Trigger(
        nextptr=ontrue,
        actions=[
            SetNextPtr(brtrg, onfalse)
        ]
    )

    onfalse << NextTrigger()


def EUDJumpIfNot(conditions, onfalse):
    '''
    Jump if conditions are not met. Two triggers are executed when jumping. If
    jump conditions are met, then the following triggers are executed.

    :param conditions: No jump condition.
    :param ontrue: Trigger to execute when conditions are not met.
    '''

    brtrg = Forward()
    ontrue = Forward()

    brtrg << Trigger(
        nextptr=onfalse,
        conditions=conditions,
        actions=[
            SetNextPtr(brtrg, ontrue)
        ]
    )

    ontrue << Trigger(
        actions=[
            SetNextPtr(brtrg, onfalse)
        ]
    )
