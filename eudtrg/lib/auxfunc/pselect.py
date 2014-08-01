from eudtrg import LICENSE  # @UnusedImport

from eudtrg.base import *  # @UnusedWildImport
from eudtrg.lib.baselib import *  # @UnusedWildImport

from .readdword import f_dwread


def InitPlayerSwitch(playerroots):
    '''
    Override default behavior of :func:`SaveMap` and set starting trigger for
    all players.

    :param playerroots: Starting trigger for each players. (List of 8 elements)
        Starting trigger may be None if the player won't execute any trigger.
    :returns: Starting trigger for InitPlayerSwitch to work.

    .. warning::
        You should call InitPlayerSwitch at most once.
    '''
    PushTriggerScope()
    playerroots = [p if p else Trigger(nextptr=triggerend) for p in playerroots]
    PopTriggerScope()

    vt = EUDVTable(8)
    ptsfirst = vt.GetVariables()

    # Read first trigger of every players.
    psbegin = NextTrigger()

    for i in range(8):
        SetVariables(ptsfirst[i], f_dwread(EPD(0x51A280 + 8 + 12 * i)))

    # Create trigger skipper to prevent memory leak
    playerentry = [Forward() for _ in range(8)]
    playerentry2 = [Forward() for _ in range(8)]
    entry2_act1 = [Forward() for _ in range(8)]

    PushTriggerScope()
    for i in range(8):
        playerentry[i] << Trigger(
            nextptr=0,  # 0 will be ptsfirst[i]
            actions=[
                SetNextPtr(playerentry[i], playerentry2[i])
            ]
        )

        playerentry2[i] << Trigger(
            nextptr=playerroots[i],
            actions=[
                # 0 will be ptsfirst[i]
                entry2_act1[i] << SetNextPtr(playerentry[i], 0)
            ]
        )

    PopTriggerScope()

    SeqCompute(
        # modify playerentry[i].prev
        [(EPD(playerentry[i] + 0), SetTo, 0x51A280 + 12 * i + 4) for i in range(8)] +
        # modify playerentry[i].next
        [(EPD(playerentry[i] + 4), SetTo, ptsfirst[i]) for i in range(8)] +
        # modify entry2_act1.number
        [(EPD(entry2_act1[i] + 20), SetTo, ptsfirst[i]) for i in range(8)] +
        [(EPD(0x51A280 + 12 * i + 8), SetTo, playerentry[i])
         for i in range(8)]       # Modify pts
    )

    for i in range(8):
        t = Forward()
        # If pts was empty (pts->lasttrig == pts)
        EUDJumpIfNot(
            Memory(0x51A280 + 12 * i + 4, Exactly, 0x51A280 + 12 * i + 4), t)
        SeqCompute([(EPD(0x51A280 + 12 * i + 4), SetTo, playerentry[i])])
        t << NextTrigger()

    Trigger(
        nextptr=triggerend,
        actions=[
            SetDeaths(203151, SetTo, 0, 0)  # SetDeaths thing
        ]
    )

    return psbegin
