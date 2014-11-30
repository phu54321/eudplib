from ... import core as c
from ... import ctrlstru as cs

jumper = None


def _MainStarter(mf):
    global jumper

    c.PushTriggerScope()

    jumper = c.Forward()
    rootstarter = c.NextTrigger()
    mf()
    c.Trigger(
        nextptr=0x80000000,
        actions=c.SetNextPtr(jumper, 0x80000000)
    )

    # Jumper
    jumper << c.Trigger(nextptr=rootstarter)

    c.PopTriggerScope()

    return rootstarter


def DoEvents():
    _t = c.Forward()
    cs.DoActions(c.SetNextPtr(jumper, _t))
    cs.EUDJump(0x80000000)
    _t << c.NextTrigger()
