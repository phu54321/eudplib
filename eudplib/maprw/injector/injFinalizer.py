#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from ... import core as c
from ... import ctrlstru as cs
from ... import eudlib as sf
from eudplib import utils as ut
from ...trigtrg import runtrigtrg as rtt

from ..inlinecode import PreprocessTrigSection


_inlineCodes = []


''' Stage 3:
- Fixes nextptr modification to TRIG triggers by stage 1
- Flip property value by trig section
- Dispatch inline codes
- Create infinite executer for root
'''


def _DispatchInlineCode(trigepd):
    global _inlineCodes

    trigepdPlus1 = trigepd + 1

    funcCode = sf.f_dwread_epd(trigepd + 2)
    nextptr = sf.f_dwread_epd(trigepdPlus1)
    end = c.Forward()

    # To reduce trigger usage, we use current player trick here
    cs.DoActions(c.SetMemory(0x6509B0, c.SetTo, trigepd))

    for funcID, func in _inlineCodes:
        if cs.EUDIf()(funcCode == funcID):
            # Generate kicker
            codeStart, codeEnd = func

            cs_a0_epd = ut.EPD(codeStart) + (8 + 320) // 4

            cs.DoActions([
                # SetNextPtr for this trigger
                # action #1
                c.SetMemory(0x6509B0, c.Add, (8 + 320 + 32 * 0) // 4 + 4),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, trigepdPlus1),
                c.SetMemory(0x6509B0, c.Add, 1),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, codeStart),

                # SetNextPtr for codeend
                # action #2
                c.SetMemory(0x6509B0, c.Add, 7),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, ut.EPD(codeEnd) + 1),
                c.SetMemory(0x6509B0, c.Add, 1),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, nextptr),

                # This trigger sets argument for cs_a0_epd
                # cs_a0 will be SetNextPtr(trigepd + 1, nextptr) after this
                # action #3
                c.SetMemory(0x6509B0, c.Add, 7),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, cs_a0_epd + 4),
                c.SetMemory(0x6509B0, c.Add, 1),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, trigepdPlus1),

                # action #4
                c.SetMemory(0x6509B0, c.Add, 7),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, cs_a0_epd + 5),
                c.SetMemory(0x6509B0, c.Add, 1),
                c.SetMemoryEPD(c.CurrentPlayer, c.SetTo, nextptr),
            ])
            cs.EUDJump(end)
        cs.EUDEndIf()



    end << c.NextTrigger()


@c.EUDFunc
def _FlipProp(trigepd):
    '''Iterate through triggers and flip 'Trigger disabled' flag

    Also, dispatch inline codes
    '''

    if cs.EUDWhileNot()([trigepd >= 0x3FD56E6E, trigepd <= 0x3FD56E86]):
        prop_epd = trigepd + (8 + 320 + 2048) // 4
        # trigepd's nextptr may change during flipping process, so
        # we get it now.
        nexttrigepd = sf.f_epdread_epd(trigepd + (4 // 4))

        if cs.EUDIf()(c.Deaths(prop_epd, c.Exactly, 4, 0)):  # Preserved
            sf.f_dwwrite_epd(prop_epd, 8)  # Disable now
        if cs.EUDElse()():
            sf.f_dwsubtract_epd(prop_epd, 8)
        cs.EUDEndIf()

        # Dispatch inline code
        if cs.EUDIf()(c.Deaths(prop_epd, c.Exactly, 0x10000000, 0)):
            sf.f_dwwrite_epd(prop_epd, 4)  # Preserve
            _DispatchInlineCode(trigepd)
        cs.EUDEndIf()

        trigepd << nexttrigepd

    cs.EUDEndWhile()


def CreateInjectFinalizer(chkt, root):
    pts = 0x51A280

    # Apply inline code patch
    global _inlineCodes
    trigSection = chkt.getsection('TRIG')
    _inlineCodes, trigSection = PreprocessTrigSection(trigSection)
    chkt.setsection('TRIG', trigSection)

    if c.PushTriggerScope():
        ret = c.NextTrigger()

        # Revert nextptr
        triggerend = sf.f_dwread_epd(9)
        ptsprev_epd = sf.f_dwread_epd(10)
        sf.f_dwwrite_epd(ptsprev_epd, triggerend)
        cs.DoActions([
            c.SetDeaths(9, c.SetTo, 0, 0),
            c.SetDeaths(10, c.SetTo, 0, 0)
        ])

        # revert mrgndata
        mrgndata = chkt.getsection('MRGN')
        mrgndata_db = c.Db(mrgndata)
        sf.f_repmovsd_epd(ut.EPD(0x58DC60), ut.EPD(mrgndata_db), 5100 // 4)

        # Flip TRIG properties
        i = c.EUDVariable()
        if cs.EUDWhile()(i <= 7):
            _FlipProp(sf.f_epdread_epd(ut.EPD(pts + 8) + i + i + i))
            i << i + 1
        cs.EUDEndWhile()

        # Create payload for each players & Link them with pts
        lasttime = c.EUDVariable()
        curtime = c.EUDVariable()
        tmcheckt = c.Forward()

        for player in range(8):
            trs = rtt._runner_start[player]
            tre = rtt._runner_end[player]

            c.PushTriggerScope()

            # Crash preventer
            tstart, _t0 = c.Forward(), c.Forward()
            tstart << c.RawTrigger(
                prevptr=pts + player * 12 + 4,
                nextptr=trs,
                actions=[c.SetNextPtr(tstart, _t0)]
            )

            _t0 << c.RawTrigger(
                nextptr=tmcheckt,
                actions=[
                    # reset
                    c.SetNextPtr(tstart, trs)
                ]
            )

            c.PopTriggerScope()

            prevtstart = sf.f_dwread_epd(ut.EPD(pts + player * 12 + 8))
            prevtend = sf.f_dwread_epd(ut.EPD(pts + player * 12 + 4))

            # If there were triggers
            if cs.EUDIfNot()(prevtstart == ~(pts + player * 12 + 4)):
                # Modify pts
                c.SeqCompute([
                    (ut.EPD(pts + player * 12 + 8), c.SetTo, tstart),
                    (ut.EPD(pts + player * 12 + 4), c.SetTo, tre),
                ])

                # link trs, tre with them
                c.SeqCompute([
                    (ut.EPD(trs + 4), c.SetTo, prevtstart),
                ])
                sf.f_dwwrite_epd(ut.EPD(prevtend) + 1, tre)
            cs.EUDEndIf()

        if c.PushTriggerScope():
            tmcheckt << c.NextTrigger()
            curtime << sf.f_dwread_epd(ut.EPD(0x57F23C))
            if cs.EUDIf()(lasttime < curtime):
                lasttime << curtime
                cs.EUDJump(root)
            cs.EUDEndIf()

            # Set current trigger to 1.
            cs.DoActions(c.SetMemory(0x6509B0, c.SetTo, 0))

            cs.EUDJump(0x80000000)
        c.PopTriggerScope()

        # lasttime << curtime
        curtime << sf.f_dwread_epd(ut.EPD(0x57F23C))
        lasttime << curtime

        cs.DoActions(c.SetMemory(0x6509B0, c.SetTo, 0))  # Current player = 1

        # now jump to root
        cs.EUDJump(root)

    c.PopTriggerScope()

    return ret
