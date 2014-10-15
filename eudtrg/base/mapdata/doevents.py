from ..dataspec.trigger import (
    Trigger,
    NextTrigger,
    PushTriggerScope,
    PopTriggerScope,
    triggerend
)

from ..dataspec.forward import Forward
from ..dataspec.bytedump import Db
from ..stocktrg import *

PushTriggerScope()
oepjmpflag = 0x58A380
oepjumper1 = Forward()
oepjumper1 << Trigger(
    conditions=Memory(oepjmpflag, Exactly, 1),
    actions=SetNextPtr(oepjumper1, triggerend)
)
oepjumper2 = Trigger(
    actions=SetMemory(oepjmpflag, SetTo, 1)
)
PopTriggerScope()


def CreateTriggerStarter(root, injector):
    global oepjumper1, oepjumper2

    # Add crash killer in front of the trigger
    triggerend = ~(0x51A284 + injector * 12)

    # For programs who missed putting triggerend to their last trigger.

    PushTriggerScope()

    entry1 = Forward()
    entry2 = Forward()
    entry3 = Forward()

    entry1 << Trigger(
        nextptr=triggerend,
        actions=[
            SetNextPtr(entry1, entry2)
        ]
    )

    entry2 << Trigger(
        actions=SetNextPtr(entry1, triggerend)
    )

    entry3 << Trigger(
        nextptr=oepjumper1,
        actions=[
            SetNextPtr(oepjumper2, root),
            SetNextPtr(entry2, oepjumper1)
        ]
    )

    PopTriggerScope()

    return entry1


def EUDDoEvents():
    nexttrg = Forward()

    Trigger(
        nextptr=triggerend,
        actions=[
            SetNextPtr(oepjumper2, nexttrg),
            SetMemory(oepjmpflag, SetTo, 0)
        ]
    )

    nexttrg << NextTrigger()
