#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''

import struct

from ... import core as c
from ... import eudlib as sf
from ... import ctrlstru as cs
from ... import varfunc as vf
from ... import trigger as trig

cargs = [
    0x08D3DCB1,
    0x05F417D1,
    0x01886E5F,
    0x01539095,
    0x00980E41,
    0x006D0B81,
    0x0060CDB5,
    0x0059686D,
    0x0045A523,
    0x0041BBB3,
]

@c.EUDFunc
def f_verify(payload_epd, dwn):
    counts = c.EUDCreateVariables(len(cargs))
    t = [c.Forward() for _ in range(len(cargs))]
    trig.Trigger(
        actions=[
            [
                c.SetMemory(t[i] + 4, c.SetTo, payload_epd),
                c.SetMemory(t[i] + 8, c.SetTo, 12345 * carg),
                counts[i].SetNumber(0),
            ]
            for i, carg in enumerate(cargs)
        ]
    )

    if cs.EUDWhile(dwn > 0):
        # Functionally equivilant to:
        #   for i in range(len(cargs)):
        #       if dw >= compv[i]:
        #           counts[i] += 1
        #       compv[i] = (compv[i] + cargs[i]) & 0xFFFFFFFF
        for i in range(len(cargs)):
            c.RawTrigger(
                conditions=[
                    t[i] << c.Memory(0, c.AtLeast, 0)
                ],
                actions=[
                    counts[i].AddNumber(1),
                ]
            )

        # i++
        c.RawTrigger(
            actions=[
                [
                    c.SetMemory(t[i] + 4, c.Add, 1),
                    c.SetMemory(t[i] + 8, c.Add, carg)
                ]
                for i, carg in enumerate(cargs)
            ] + [
                dwn.SubtractNumber(1)
            ]
        )
    cs.EUDEndWhile()

    return counts


def verifyf(buf):
    counts = [0] * len(cargs)
    dwn = len(buf) // 4
    dwlist = struct.unpack('%dL' % dwn, buf)

    for i, carg in enumerate(cargs):
        compv = (12345 * carg) & 0xFFFFFFFF
        count = 0
        for dw in dwlist:
            if dw >= compv:
                count += 1
            compv = (compv + carg) & 0xFFFFFFFF
        counts[i] = count

    return counts

def CreateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.prttable]))
    prtn = vf.EUDVariable()

    ortdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.orttable]))
    ortn = vf.EUDVariable()

    orig_payload = c.Db(payload.data)

    c.PushTriggerScope()

    root = c.NextTrigger()

    '''
    # TODO : make verifyf faster and re-enable this code
    #
    # Verify payload
    # Note : this is very, very basic protection method. Intended attackers should be
    # able to penetrate through this very easily
    vchks = f_verify(c.EPD(orig_payload), len(payload.data) // 4)
    origchks = verifyf(payload.data)
    trig.Trigger(actions=[
        c.SetDeaths(i, c.SetTo, vchk, 1)
        for i, vchk in enumerate(vchks)
    ])
    if cs.EUDIfNot([origchk == vchk for origchk, vchk in zip(origchks, vchks)]):
        cs.DoActions([
            c.Defeat(),
            c.SetMemory(0, c.SetTo, 0),
        ])
    cs.EUDEndIf()
    '''

    prtn << len(payload.prttable)
    ortn << len(payload.orttable)

    # init prt
    if payload.prttable:
        if cs.EUDInfLoop():
            cs.DoActions(prtn.SubtractNumber(1))
            sf.f_dwadd_epd(
                c.EPD(orig_payload) + sf.f_dwread_epd(prtn + c.EPD(prtdb)),
                orig_payload // 4
            )
            cs.EUDLoopBreakIf(prtn.Exactly(0))
        cs.EUDEndInfLoop()

    # init ort
    if payload.orttable:
        if cs.EUDInfLoop():
            cs.DoActions(ortn.SubtractNumber(1))
            sf.f_dwadd_epd(
                c.EPD(orig_payload) + sf.f_dwread_epd(ortn + c.EPD(ortdb)),
                orig_payload
            )
            cs.EUDLoopBreakIf(ortn.Exactly(0))
        cs.EUDEndInfLoop()

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()
    return c.CreatePayload(root)

