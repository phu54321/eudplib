#!/usr/bin/python
# -*- coding: utf-8 -*-

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
