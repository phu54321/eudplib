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

from .. import core as c
from ..utils.blockstru import (
    BlockStruManager,
    SetCurrentBlockStruManager,
)

from ..core.mapdata import mapdata, mpqapi

from .injector.vectorReloc import CreateVectorRelocator
from .injector.payloadReloc import CreatePayloadRelocator
from .injector.injFinalizer import CreateInjectFinalizer
from .injector.doevents import _MainStarter


def SaveMap(fname, rootf):
    print('Saving to %s...' % fname)
    chkt = mapdata.GetChkTokenized()

    # Create injector triggers
    bsm = BlockStruManager()
    prev_bsm = SetCurrentBlockStruManager(bsm)

    if c.PushTriggerScope():
        root = _MainStarter(rootf)
        root = CreateInjectFinalizer(chkt, root)
    c.PopTriggerScope()
    payload = c.CreatePayload(root)

    c.PushTriggerScope()
    final_payload = CreatePayloadRelocator(payload)
    c.PopTriggerScope()
    SetCurrentBlockStruManager(prev_bsm)

    # Update string table & etc
    # User-defined strings in eudplib program is registered after rootf is
    # called. This happens when _MainStarter is called, so UpdateMapData
    # function should be called after `doevents._MainStarter(rootf)` call.
    mapdata.UpdateMapData()
    # stage1.CreateAndApplyStage1 requires STR section to be constructed before
    # it append stage2 payload after 'original' STR section. so UpdateMapData
    # should be called before `stage1.CreateAndApplyStage1`.

    # Create and apply stage 1 payload.
    # Stage 1 initializes stage 2 (real payload initializer)
    CreateVectorRelocator(chkt, final_payload)

    chkt.optimize()
    rawchk = chkt.savechk()
    print('Output scenario.chk : %.3fMB' % (len(rawchk) / 1000000))

    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()
