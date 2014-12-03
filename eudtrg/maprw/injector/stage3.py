#!/usr/bin/python
#-*- coding: utf-8 -*-

''' Stage 3:
- Fixes nextptr modification to TRIG triggers by stage 1
- Flip property value by trig section
- Create infinite executer for root
'''

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf
from ... import stdfunc as sf


@vf.EUDFunc
def FlipProp(initptr):
    '''Iterate through triggers and flip 'Trigger disabled' flag'''

    if cs.EUDWhile(initptr <= 0x7FFFFFFF):
        initepd = sf.f_epd(initptr)

        prop_epd = initepd + (8 + 320 + 2048) // 4
        propv = sf.f_dwread_epd(prop_epd)
        sf.f_dwwrite_epd(prop_epd, sf.f_bitxor(propv, 8))  # Flip bit 3

        initptr << sf.f_dwread_epd(initepd + (4 // 4))

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
        FlipProp(sf.f_dwread_epd(c.EPD(pts + 8) + i + i + i))
        i << i + 1
    cs.EUDEndWhile()

    # Create payload for each players & Link them with pts
    lasttime = vf.EUDVariable()
    curtime = vf.EUDVariable()

    for player in range(8):
        if c.PushTriggerScope():  # Crash preventer code

            # Crash preventer
            tstart, _t0 = c.Forward(), c.Forward()
            tstart << c.Trigger(
                prevptr=pts + player * 12 + 4,
                nextptr=0,  # 0 -> pts[player].prev
                actions=[c.SetNextPtr(tstart, _t0)]
            )

            _t0 << c.Trigger(
                actions=[
                    c.SetNextPtr(tstart, 0)  # 0 -> pts[player].prev
                ]
            )

            # Time checker -> ensure that STR trigger is executed only once.
            curtime << sf.f_dwread_epd(c.EPD(0x57F23C))
            if cs.EUDIf(lasttime < curtime):
                lasttime << curtime
                cs.EUDJump(root)
            cs.EUDEndIf()

            cs.EUDJump(0x80000000)

        c.PopTriggerScope()

        prevtstart = sf.f_dwread_epd(c.EPD(pts + player * 12 + 8))
        if cs.EUDIfNot(prevtstart == pts + player * 12 + 4):
            vf.SeqCompute([
                (c.EPD(pts + player * 12 + 8), c.SetTo, tstart),
                (c.EPD(tstart + 4), c.SetTo, prevtstart),
                (c.EPD(_t0 + 8 + 320 + 20), c.SetTo, prevtstart)
            ])
        cs.EUDEndIf()

    # lasttime << curtime
    curtime << sf.f_dwread_epd(c.EPD(0x57F23C))
    lasttime << curtime

    # now jump to root
    cs.EUDJump(root)

    c.PopTriggerScope()

    return ret
