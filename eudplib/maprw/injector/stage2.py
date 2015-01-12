#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''

from ... import core as c
from ... import stdfunc as sf
from ... import ctrlstru as cs
from ... import varfunc as vf


@c.EUDFunc
def f_fletcher64(payload_epd, dwn):
    a = c.EUDVariable()
    b = c.EUDVariable()
    a << 0xF65411E5
    b << 0x4A00C740

    if cs.EUDWhile(dwn > 0):

        tmpa = a + sf.f_dwread_epd(payload_epd)
        c.RawTrigger(conditions=tmpa < a, actions=tmpa.AddNumber(1))
        a << tmpa

        tmpb = b + a
        c.RawTrigger(conditions=tmpb < b, actions=tmpb.AddNumber(1))
        b << tmpb

        payload_epd += 1
        dwn -= 1
    cs.EUDEndWhile()

    return a, b


def fl64(b):
    a = 0xF65411E5
    b = 0x4A00C740
    dwn = len(b) // 4

    for i in range(dwn):
        a = (a + c.b2i4(b, i * 4)) % 0xFFFFFFFF
        b = (b + a) % 0xFFFFFFFF
    return a, b


def CreateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.prttable]))
    prtn = vf.EUDVariable()

    ortdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.orttable]))
    ortn = vf.EUDVariable()

    orig_payload = c.Db(payload.data)

    c.PushTriggerScope()

    root = c.NextTrigger()

    # Checksum
    chka, chkb = fl64(payload.data)
    fla, flb = f_fletcher64(c.EPD(orig_payload), len(orig_payload) // 4)
    if cs.EUDIfNot([fla == chka, flb == chkb]):
        cs.DoActions(cs.SetDeaths(0, SetTo, 0))
    cs.EUDEndIf()

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

    ####
    # return c.CreatePayload(root)
    ####

    payload = c.CreatePayload(root)
    open('out.bin', 'wb').write(payload.data)
    return payload
