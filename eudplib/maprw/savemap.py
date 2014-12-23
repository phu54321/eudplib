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
from .. import varfunc as vf
from ..core.mapdata import mapdata, mpqapi
from .injector import stage1, stage2, stage3, doevents


def SaveMap(fname, rootf):
    print('Saving to %s...' % fname)
    chkt = mapdata.GetChkTokenized()

    # Create injector triggers
    bsm = c.BlockStruManager()
    prev_bsm = c.SetCurrentBlockStruManager(bsm)

    c.PushTriggerScope()
    root = doevents._MainStarter(rootf)
    root = stage3.CreateStage3(root, chkt.getsection('MRGN'))
    c.PopTriggerScope()
    payload = c.CreatePayload(root)

    c.PushTriggerScope()
    final_payload = stage2.CreateStage2(payload)
    c.PopTriggerScope()
    c.SetCurrentBlockStruManager(prev_bsm)

    # Update string table & etc
    # User-defined strings in eudplib program is registered after rootf is
    # called. This happens when _MainStarter is called, so UpdateMapData function should
    # be called after `doevents._MainStarter(rootf)` call.
    mapdata.UpdateMapData()
    # stage1.CreateAndApplyStage1 requires STR section to be constructed before
    # it append stage2 payload after 'original' STR section. so UpdateMapData
    # should be called before `stage1.CreateAndApplyStage1`.

    # Create and apply stage 1 payload.
    # Stage 1 initializes stage 2 (real payload initializer)
    stage1.CreateAndApplyStage1(chkt, final_payload)

    chkt.optimize()
    rawchk = chkt.savechk()
    print('Output scenario.chk : %.3fMB' % (len(rawchk) / 1000000))

    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk)
    mw.Compact()
    mw.Close()
