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
from ... import eudlib as sf
from ... import ctrlstru as cs
from ... import varfunc as vf
from ... import trigger as trig
from ... import utils as ut
from .verifyf import verifyf

''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''

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


def CreateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([ut.i2b4(x // 4) for x in payload.prttable]))
    prtn = vf.EUDVariable()

    ortdb = c.Db(b''.join([ut.i2b4(x // 4) for x in payload.orttable]))
    ortn = vf.EUDVariable()

    orig_payload = c.Db(payload.data)

    c.PushTriggerScope()

    root = c.NextTrigger()

    # Verify payload
    # Note : this is very, very basic protection method. Intended attackers
    # should be able to penetrate through this very easily
    vchks = f_verify(ut.EPD(orig_payload), len(payload.data) // 4)
    origchks = verifyf(bytearray(payload.data), len(payload.data))

    trig.Trigger(actions=[
        c.SetDeaths(i, c.SetTo, vchk, 1)
        for i, vchk in enumerate(vchks)
    ])
    if cs.EUDIfNot(
        [origchk == vchk for origchk, vchk in zip(origchks, vchks)]
    ):
        cs.DoActions([
            c.Defeat(),
            c.SetMemory(0, c.SetTo, 0),
        ])
    cs.EUDEndIf()

    # init prt
    prtn << len(payload.prttable)
    if payload.prttable:
        if cs.EUDInfLoop():
            cs.DoActions(prtn.SubtractNumber(1))
            sf.f_dwadd_epd(
                ut.EPD(orig_payload) + sf.f_dwread_epd(prtn + ut.EPD(prtdb)),
                orig_payload // 4
            )
            cs.EUDLoopBreakIf(prtn.Exactly(0))
        cs.EUDEndInfLoop()

    # init ort
    ortn << len(payload.orttable)
    if payload.orttable:
        if cs.EUDInfLoop():
            cs.DoActions(ortn.SubtractNumber(1))
            sf.f_dwadd_epd(
                ut.EPD(orig_payload) + sf.f_dwread_epd(ortn + ut.EPD(ortdb)),
                orig_payload
            )
            cs.EUDLoopBreakIf(ortn.Exactly(0))
        cs.EUDEndInfLoop()

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()
    return c.CreatePayload(root)
