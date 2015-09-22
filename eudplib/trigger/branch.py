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
from eudplib import utils as ut
from .tpatcher import PatchCondition


def Branch(conditions, ontrue, onfalse):
    flag = c.EUDLightVariable()
    flag << 0

    conditions = ut.FlattenList(conditions)

    if len(conditions) == 0:
        c.RawTrigger(nextptr=ontrue)  # Just jump
        return

    brtriggers = []
    onfalsetrg = c.Forward()

    # Check all conditions
    for i in range(0, len(conditions), 16):
        conds = conditions[i:i + 16]
        patched_conds = []
        for cond in conds:
            patched_conds.append(PatchCondition(cond))

        brtrg = c.Forward()
        nxtrg = c.Forward()
        brtrg << c.RawTrigger(
            nextptr=onfalsetrg,
            conditions=patched_conds,
            actions=c.SetNextPtr(brtrg, nxtrg)
        )

        nxtrg << c.NextTrigger()
        brtriggers.append(brtrg)

    # On true : revert all
    revertacts = [c.SetNextPtr(brtrg, onfalsetrg) for brtrg in brtriggers]
    for i in range(0, len(revertacts), 64):
        if i + 64 < len(revertacts):
            c.RawTrigger(actions=revertacts[i:i + 64])
        else:
            c.RawTrigger(nextptr=ontrue, actions=revertacts[i:i + 64])

    # on false
    if len(brtriggers) >= 2:
        onfalsetrg << c.NextTrigger()
        # Revert all except last brtrg
        revertacts = [c.SetNextPtr(brtrg, onfalsetrg)
                      for brtrg in brtriggers][:-1]
        for i in range(0, len(revertacts), 64):
            if i + 64 < len(revertacts):
                c.RawTrigger(actions=revertacts[i:i + 64])
            else:
                c.RawTrigger(nextptr=onfalsetrg, actions=revertacts[i:i + 64])
    else:
        onfalsetrg << onfalse
