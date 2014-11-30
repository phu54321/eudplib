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

    if cs.EUDWhileNot(initptr <= 0x7FFFFFFF):
        initepd = sf.f_epd(initptr)

        prop_epd = initepd + (8 + 320 + 2048) // 4
        propv = sf.f_dwread_epd(prop_epd)
        sf.f_dwwrite_epd(prop_epd, sf.f_bitxor(propv, 8))  # Flip bit 3

        initptr << sf.f_epd(sf.f_dwread_epd(initepd + (4 // 4)))

    cs.EUDEndWhile()


def CreateStage3(root):
    c.PushTriggerScope()

    ret = c.NextTrigger()

    c.Trigger(actions=c.SetDeaths(5, c.SetTo, 1234, 0))

    # Revert nextptr
    triggerend = sf.f_dwread_epd(9)
    ptsprev_epd = sf.f_dwread_epd(10)
    sf.f_dwwrite_epd(ptsprev_epd, triggerend)

    # Flip TRIG properties
    i = vf.EUDVariable()
    if cs.EUDWhile(i <= 7):
        FlipProp(c.EPD(0x51A288) + i + i + i)
        i << i + 1
    cs.EUDEndWhile()

    # Create payload for each players & Link them with pts
    lasttime = vf.EUDVariable()
    curtime = vf.EUDVariable()
    prevtstart = vf.EUDVariable()
    pts = 0x0051A280

    for player in range(8):
        c.PushTriggerScope()

        # Crash preventer
        tstart, _t0 = c.Forward(), c.Forward()
        tstart << c.Trigger(
            nextptr=0,
            actions=[c.SetNextPtr(tstart, _t0)]
        )

        _t0 << c.Trigger(
            actions=[
                c.SetNextPtr(tstart, 0)
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

        prevtstart << sf.f_dwread_epd(c.EPD(player + pts * 12 + 8))

        vf.SeqCompute([
            (c.EPD(player + pts * 12 + 8), c.SetTo, tstart),
            (c.EPD(tstart + 4), c.SetTo, prevtstart),
            (c.EPD(_t0 + 8 + 320 + 20), c.SetTo, prevtstart)
        ])

    # pts initialized. now jump to root
    cs.EUDJump(root)

    c.PopTriggerScope()

    return ret
