#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Stage 1 : works in TRIG section.
- Check if EUD is available. If not, defeat
- Initialize stage 2 & execute it
- Modifies TRIG trigger's nextptr. Modification is fixed in stage 3.
'''

from ... import core as c
from ...trigtrg import trigtrg as tt


trglist = []


def Trigger(*args, **kwargs):
    global trglist
    trglist.append(tt.Trigger(*args, **kwargs))


def CopyDeaths(iplayer, oplayer, copyepd=False, initvalue=None):
    tmpplayer = 11

    if initvalue is None:
        if copyepd:
            initvalue = tt.EPD(0)
        else:
            initvalue = 0

    Trigger(
        actions=[
            tt.SetDeaths(oplayer, tt.SetTo, initvalue, 0),
            tt.SetDeaths(tmpplayer, tt.SetTo, 0, 0),
        ]
    )

    for i in range(31, 1, -1):
        if copyepd:
            subval = 2 ** (i - 2)

        else:
            subval = 2 ** i

        Trigger(
            conditions=[tt.Deaths(iplayer, tt.AtLeast, 2 ** i, 0)],
            actions=[
                tt.SetDeaths(iplayer, tt.Subtract, 2 ** i, 0),
                tt.SetDeaths(tmpplayer, tt.Add, 2 ** i, 0),
                tt.SetDeaths(oplayer, tt.Add, subval, 0),
            ]
        )

    for i in range(31, 1, -1):
        Trigger(
            players=[tt.AllPlayers],
            conditions=[tt.Deaths(tmpplayer, tt.AtLeast, 2 ** i, 0)],
            actions=[
                tt.SetDeaths(iplayer, tt.Add, 2 ** i, 0),
                tt.SetDeaths(tmpplayer, tt.Subtract, 2 ** i, 0),
            ]
        )


def CreateAndApplyStage1(chkt, payload_stage2):
    global trglist

    # Append 'Require EUD enabler' string.
    str_section = chkt.getsection('STR')
    strtb = c.TBL(str_section)
    eude_needed = strtb.GetStringIndex('This map requires EUD Enabler to run')
    str_section = strtb.SaveTBL()

    payload_offset = (len(str_section) + 3) & ~3
    padding_length = payload_offset - len(str_section)
    str_section = str_section + bytes(padding_length) + payload_stage2.data
    chkt.setsection('STR', str_section)

    # MAIN STAGE
    trglist.clear()

    # Check if epd is supported

    Trigger(actions=[
        tt.SetDeaths(-12, tt.SetTo, 1, 1)
    ])

    Trigger(
        conditions=[
            tt.Deaths(0, tt.Exactly, 0, 0)
        ],
        actions=[
            tt.DisplayTextMessage(eude_needed),
            tt.Draw()
        ]
    )

    Trigger(actions=[
        tt.SetDeaths(-12, tt.SetTo, 0, 1)
    ])

    # -------

    # Payload update
    curpl = 0x6509B0
    strs = 0x5993D4
    pts = 0x51A280

    CopyDeaths(tt.EPD(strs), tt.EPD(curpl), True, tt.EPD(payload_offset))

    # Init prt
    for i in range(0, len(payload_stage2.prttable), 31):
        prttb = [x // 4 for x in payload_stage2.prttable[i:i + 31]]
        Trigger(actions=tt.SetMemory(curpl, tt.Add, prttb[0]))

        # Add by payload_offset // 4
        Trigger(actions=[
            (
                tt.SetDeaths(tt.CurrentPlayer, tt.Add, payload_offset // 4, 0),
                tt.SetMemory(curpl, tt.Add,
                             prttb[i + 1 - len(prttb)] - prttb[i])
            ) for i in range(len(prttb))
        ])

        # Add by value(strs) // 4
        for e in range(31, 1, -1):
            Trigger(
                conditions=tt.Memory(strs, tt.AtLeast, 2 ** e),
                actions=[(
                             tt.SetDeaths(tt.CurrentPlayer, tt.Add, 2 ** (e - 2), 0),
                             tt.SetMemory(curpl, tt.Add,
                                          prttb[i + 1 - len(prttb)] - prttb[i])
                         ) for i in range(len(prttb))] +
                        [
                            tt.SetDeaths(11, tt.Add, 2 ** e, 0),
                            tt.SetMemory(strs, tt.Subtract, 2 ** e)
                        ]
            )

        # Revert value(strs)
        for e in range(31, 1, -1):
            Trigger(
                conditions=tt.Deaths(11, tt.AtLeast, 2 ** e, 0),
                actions=[
                    tt.SetDeaths(11, tt.Subtract, 2 ** e, 0),
                    tt.SetMemory(strs, tt.Add, 2 ** e)
                ]
            )

        Trigger(actions=tt.SetMemory(curpl, tt.Add, -prttb[0]))

    # -------

    # Init orttable
    for i in range(0, len(payload_stage2.orttable), 31):
        orttb = [x // 4 for x in payload_stage2.orttable[i:i + 31]]
        Trigger(actions=tt.SetMemory(curpl, tt.Add, orttb[0]))

        # Add by payload_offset // 4
        Trigger(actions=[
            (
                tt.SetDeaths(tt.CurrentPlayer, tt.Add, payload_offset, 0),
                tt.SetMemory(curpl, tt.Add,
                             orttb[i + 1 - len(orttb)] - orttb[i])
            ) for i in range(len(orttb))
        ])

        # Add by value(strs) // 4
        for e in range(31, 1, -1):
            Trigger(
                conditions=tt.Memory(strs, tt.AtLeast, 2 ** e),
                actions=[(
                             tt.SetDeaths(tt.CurrentPlayer, tt.Add, 2 ** e, 0),
                             tt.SetMemory(curpl, tt.Add,
                                          orttb[i + 1 - len(orttb)] - orttb[i])
                         ) for i in range(len(orttb))] +
                        [
                            tt.SetDeaths(11, tt.Add, 2 ** e, 0),
                            tt.SetMemory(strs, tt.Subtract, 2 ** e)
                        ]
            )

        # Revert value(strs)
        for e in range(31, 1, -1):
            Trigger(
                conditions=tt.Deaths(11, tt.AtLeast, 2 ** e, 0),
                actions=[
                    tt.SetDeaths(11, tt.Subtract, 2 ** e, 0),
                    tt.SetMemory(strs, tt.Add, 2 ** e)
                ]
            )

        Trigger(actions=tt.SetMemory(curpl, tt.Add, -orttb[0]))

    # -------

    # Jump to payload

    # Reset curpl
    Trigger(actions=[
        tt.SetDeaths(10, tt.SetTo, tt.EPD(4), 0),
        tt.SetMemory(curpl, tt.SetTo, tt.EPD(4)),
    ])

    for player in range(8):
        ptsprev = pts + 12 * player + 4
        triggerend = ~(0x51A284 + player * 12)

        Trigger(
            players=[player],
            actions=[
                tt.SetDeaths(9, tt.SetTo, triggerend, 0)  # Used in stage 2
            ]
        )

        # curpl += value(ptsprev) // 4
        for e in range(31, 1, -1):
            Trigger(
                players=[player],
                conditions=tt.Memory(ptsprev, tt.AtLeast, 2 ** e),
                actions=[
                    tt.SetMemory(ptsprev, tt.Subtract, 2 ** e),
                    tt.SetDeaths(10, tt.Add, 2 ** (e - 2), 0),
                    # Player 10 is used for nextptr recovery in stage 3
                    tt.SetDeaths(11, tt.Add, 2 ** e, 0),  # Temporary
                    tt.SetMemory(curpl, tt.Add, 2 ** (e - 2))
                ]
            )

        for e in range(31, 1, -1):
            Trigger(
                players=[player],
                conditions=tt.Deaths(11, tt.AtLeast, 2 ** e, 0),
                actions=[
                    tt.SetDeaths(11, tt.Subtract, 2 ** e, 0),
                    tt.SetMemory(ptsprev, tt.Add, 2 ** e),
                ]
            )

    # now curpl = EPD(value(ptsprev) + 4)
    # value(EPD(value(ptsprev) + 4)) = strs + payload_offset
    CopyDeaths(tt.EPD(strs), tt.CurrentPlayer, False, payload_offset)

    trigdata = b''.join(trglist)

    # Stage 1 created

    # -------

    # Previous trigger datas

    oldtrigraw = chkt.getsection('TRIG')
    oldtrigs = \
        [oldtrigraw[i:i + 2400] for i in range(0, len(oldtrigraw), 2400)]
    proc_trigs = []

    # Collect only enabled triggers
    for trig in oldtrigs:
        trig = bytearray(trig)
        flag = c.b2i4(trig, 320 + 2048)
        if flag & 8:  # Trigger already disabled
            pass

        flag ^= 8
        trig[320 + 2048: 320 + 2048 + 4] = c.i2b4(flag)
        proc_trigs.append(bytes(trig))

    oldtrigraw_processed = b''.join(proc_trigs)
    chkt.setsection('TRIG', trigdata + oldtrigraw_processed)
