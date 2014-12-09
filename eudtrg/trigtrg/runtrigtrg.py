#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import core as c
from .. import varfunc as vf

_trigtrg_runner_start = [c.Forward() for _ in range(8)]
_trigtrg_runner_end = [c.Forward() for _ in range(8)]

c.PushTriggerScope()
for player in range(8):
    _trigtrg_runner_start[player] << c.Trigger(nextptr=_trigtrg_runner_end[player])
    _trigtrg_runner_end[player] << c.Trigger(nextptr=~(0x51A280 + player * 12 + 4))
c.PopTriggerScope()


@vf.EUDFunc
def RunTrigTrigger():
    for player in range(8):
        nt = c.Forward()
        c.Trigger(
            nextptr=_trigtrg_runner_start[player],
            actions=[
                c.SetMemory(0x6509B0, c.SetTo, player),
                c.SetNextPtr(_trigtrg_runner_end[player], nt)
            ]
        )
        nt << c.Trigger(
            actions=c.SetNextPtr(_trigtrg_runner_end[player], ~(0x51A280 + player * 12 + 4))
        )
