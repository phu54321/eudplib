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
from eudplib import utils as ut

''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it
'''


def CreatePayloadRelocator(payload):
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

    # init prt
    prtn << len(payload.prttable)
    if payload.prttable:
        if cs.EUDInfLoop()():
            cs.DoActions(prtn.SubtractNumber(1))
            sf.f_dwadd_epd(
                ut.EPD(orig_payload) + sf.f_dwread_epd(prtn + ut.EPD(prtdb)),
                orig_payload // 4
            )
            cs.EUDBreakIf(prtn.Exactly(0))
        cs.EUDEndInfLoop()

    # init ort
    ortn << len(payload.orttable)
    if payload.orttable:
        if cs.EUDInfLoop()():
            cs.DoActions(ortn.SubtractNumber(1))
            sf.f_dwadd_epd(
                ut.EPD(orig_payload) + sf.f_dwread_epd(ortn + ut.EPD(ortdb)),
                orig_payload
            )
            cs.EUDBreakIf(ortn.Exactly(0))
        cs.EUDEndInfLoop()

    # Jump
    cs.EUDJump(orig_payload)

    c.PopTriggerScope()
    return c.CreatePayload(root)
