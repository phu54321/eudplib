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
from .tpatcher import PatchCondition, PatchAction
from .. import utils as ut


def Trigger(conditions=None, actions=None, preserved=True):
    if conditions is None:
        conditions = []
    if actions is None:
        actions = None

    conditions = ut.FlattenList(conditions)
    actions = ut.FlattenList(actions)

    # Normal
    if len(conditions) <= 16 and len(actions) <= 64:
        for cond in conditions:
            PatchCondition(cond)

        for act in actions:
            PatchAction(act)

        c.RawTrigger(conditions=conditions, actions=actions, preserved=preserved)

    else:
        # Extended trigger
        condts = []
        cend = c.Forward()

        # Check conditions
        for i in range(0, len(conditions), 16):
            conds = conditions[i:i + 16]
            cts = c.Forward()

            for cond in conds:
                PatchCondition(cond)

            nextcond = c.Forward()
            cts << c.RawTrigger(
                nextptr=cend,
                conditions=conds,
                actions=c.SetNextPtr(cts, nextcond)
            )
            nextcond << c.NextTrigger()

            condts.append(cts)

        skipt = c.Forward()
        if not preserved:
            a = c.RawTrigger()
            c.RawTrigger(actions=c.SetNextPtr(a, skipt))

        # Execute actions
        for i in range(0, len(actions), 64):
            acts = actions[i:i + 64]
            for act in acts:
                PatchAction(act)

            c.RawTrigger(actions=acts)

        if not preserved:
            skipt << c.NextTrigger()

        # Revert conditions
        cend << c.NextTrigger()
        for i in range(0, len(condts), 64):
            c.RawTrigger(actions=[c.SetNextPtr(cts, cend) for cts in condts[i:i + 64]])

