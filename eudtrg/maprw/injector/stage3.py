#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Stage 3:
- Fixes nextptr modification to TRIG triggers by stage 1
- Flip property value by trig section
- Create infinite executer for root
'''

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf
from ... import stdfunc as sf
from ...trigtrg import runtrigtrg as rtt


@vf.EUDFunc
def FlipProp(initepd):
    '''Iterate through triggers and flip 'Trigger disabled' flag'''
    if cs.EUDWhileNot([initepd >= 0x3FD56E6E, initepd <= 0x3FD56E86]):
        prop_epd = initepd + (8 + 320 + 2048) // 4
        propv = sf.f_dwread_epd(prop_epd)

        if cs.EUDIf(propv == 4):  # Preserved
            sf.f_dwwrite_epd(prop_epd, 8)
        if cs.EUDElse():
            sf.f_dwsubtract_epd(prop_epd, 8)
        cs.EUDEndIf()

        initepd << sf.f_epdread_epd(initepd + (4 // 4))

    cs.EUDEndWhile()


def CreateStage3(root):
    pts = 0x51A280

    c.PushTriggerScope()
    ret = c.NextTrigger()

    # Revert nextptr
    triggerend = sf.f_dwread_epd(9)
    ptsprev_epd = sf.f_dwread_epd(10)
    sf.f_dwwrite_epd(ptsprev_epd, triggerend)
    cs.DoActions([
        c.SetDeaths(9, c.SetTo, 0, 0),
        c.SetDeaths(10, c.SetTo, 0, 0)
    ])

    # Flip TRIG properties
    i = vf.EUDVariable()
    if cs.EUDWhile(i <= 7):
        FlipProp(sf.f_epdread_epd(c.EPD(pts + 8) + i + i + i))
        i << i + 1
    cs.EUDEndWhile()

    # Create payload for each players & Link them with pts
    lasttime = vf.EUDVariable()
    curtime = vf.EUDVariable()
    tmcheckt = c.Forward()

    for player in range(8):
        trs = rtt._trigtrg_runner_start[player]
        tre = rtt._trigtrg_runner_end[player]

        c.PushTriggerScope()

        # Crash preventer
        tstart, _t0 = c.Forward(), c.Forward()
        tstart << c.Trigger(
            prevptr=pts + player * 12 + 4,
            nextptr=trs,
            actions=[c.SetNextPtr(tstart, _t0)]
        )

        _t0 << c.Trigger(
            nextptr=tmcheckt,
            actions=[
                # reset
                c.SetNextPtr(tstart, trs)
            ]
        )

        c.PopTriggerScope()

        prevtstart = sf.f_dwread_epd(c.EPD(pts + player * 12 + 8))
        prevtend = sf.f_dwread_epd(c.EPD(pts + player * 12 + 4))

        # Modify pts
        vf.SeqCompute([
            (c.EPD(pts + player * 12 + 8), c.SetTo, tstart),
            (c.EPD(pts + player * 12 + 4), c.SetTo, tre),
        ])

        if cs.EUDIfNot(prevtstart == ~(pts + player * 12 + 4)):  # If there were triggers
            # link trs, tre with them
            vf.SeqCompute([
                (c.EPD(trs + 4), c.SetTo, prevtstart),
            ])
            sf.f_dwwrite_epd(sf.f_epd(prevtend) + 1, tre)
        cs.EUDEndIf()

    if c.PushTriggerScope():
        tmcheckt << c.NextTrigger()
        curtime << sf.f_dwread_epd(c.EPD(0x57F23C))
        if cs.EUDIf(lasttime < curtime):
            lasttime << curtime
            cs.EUDJump(root)
        cs.EUDEndIf()

        cs.DoActions(c.SetMemory(0x6509B0, c.SetTo, 0))  # Current player = 1

        cs.EUDJump(0x80000000)
    c.PopTriggerScope()

    # lasttime << curtime
    curtime << sf.f_dwread_epd(c.EPD(0x57F23C))
    lasttime << curtime

    cs.DoActions(c.SetMemory(0x6509B0, c.SetTo, 0))  # Current player = 1

    # now jump to root
    cs.EUDJump(root)

    c.PopTriggerScope()

    return ret
