#!/usr/bin/python
#-*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs

jumper = None


def _MainStarter(mf):
    global jumper
    jumper = c.Forward()

    c.PushTriggerScope()

    rootstarter = c.NextTrigger()
    mf()
    c.Trigger(
        nextptr=0x80000000,
        actions=c.SetNextPtr(jumper, 0x80000000)
    )
    c.PopTriggerScope()

    jumper << c.Trigger(nextptr=rootstarter)
    return jumper


def EUDDoEvents():
    _t = c.Forward()
    cs.DoActions(c.SetNextPtr(jumper, _t))
    cs.EUDJump(0x80000000)
    _t << c.NextTrigger()
