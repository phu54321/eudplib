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

from eudplib import core as c
from eudplib.core.varfunc import EUDVariable, SeqCompute
from eudplib.stdfunc.calcf import f_div, f_mul
from eudplib.stdfunc.memiof import f_dwread_epd, f_dwbreak


# TODO : test this function
def VarMixedTrigger(
        conditions=None,
        actions=None,
        preserved=True
):
    if conditions is None:
        conditions = []
    if actions is None:
        actions = []

    conditions = c.FlattenList(conditions)
    actions = c.FlattenList(actions)
    trg = c.Forward()

    sqs = []
    # conditions
    for i, cond in enumerate(conditions):
        # locid
        if isinstance(cond.locid, EUDVariable):
            sqs.append((c.EPD(trg + 8 + 20 * i + 0), c.SetTo, cond.locid))
            cond.locid = 0

        # player
        if isinstance(cond.player, EUDVariable):
            sqs.append((c.EPD(trg + 8 + 20 * i + 4), c.SetTo, cond.player))
            cond.player = 0

        # amount
        if isinstance(cond.amount, EUDVariable):
            sqs.append((c.EPD(trg + 8 + 20 * i + 8), c.SetTo, cond.amount))
            cond.amount = 0

        # unitid, comparison, condtype
        if (
                        isinstance(cond.unitid, EUDVariable) or
                        isinstance(cond.comparison, EUDVariable) or
                    isinstance(cond.condtype, EUDVariable)
        ):
            cond.unitid = f_div(cond.unitid, 65536)[1]
            cond.comparison = f_div(cond.comparison, 256)[1]
            cond.condtype = f_div(cond.condtype, 256)[1]
            sqs.append((
                c.EPD(trg + 8 + 20 * i + 12),
                c.SetTo,
                f_mul(0x1000000, cond.condtype) + f_mul(0x10000, cond.comparison) + cond.unitid
            ))

            cond.unitid = 0
            cond.comparison = 0
            cond.condtype = 0

        # restype, flags
        if (
                    isinstance(cond.restype, EUDVariable) or
                    isinstance(cond.flags, EUDVariable)
        ):
            cond.restype = f_div(cond.restype, 256)[1]
            cond.flags = f_div(cond.flags, 256)[1]

            internal = f_dwbreak(f_dwread_epd(c.EPD(trg + 8 + 20 * i + 16)))[1]
            sqs.append((
                c.EPD(trg + 8 + 20 * i + 16),
                c.SetTo,
                f_mul(0x10000, internal) + (f_mul(0x100, cond.flags) + cond.restype)
            ))

            cond.restype = 0
            cond.flags = 0

    # actions
    for i, act in enumerate(actions):
        # locid1
        if isinstance(act.locid1, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 0), c.SetTo, act.locid1))
            act.locid1 = 0

        # strid
        if isinstance(act.strid, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 4), c.SetTo, act.strid))
            act.strid = 0

        # wavid
        if isinstance(act.wavid, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 8), c.SetTo, act.wavid))
            act.wavid = 0

        # time
        if isinstance(act.time, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 12), c.SetTo, act.time))
            act.time = 0

        # player1
        if isinstance(act.player1, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 16), c.SetTo, act.player1))
            act.player1 = 0

        # player2
        if isinstance(act.player2, EUDVariable):
            sqs.append((c.EPD(trg + 328 + 32 * i + 20), c.SetTo, act.player2))
            act.player2 = 0

        # unitid, acttype, amount
        if (
                        isinstance(act.unitid, EUDVariable) or
                        isinstance(act.acttype, EUDVariable) or
                    isinstance(act.amount, EUDVariable)
        ):
            act.unitid = f_div(act.unitid, 65536)[1]
            act.acttype = f_div(act.acttype, 256)[1]
            act.amount = f_div(act.amount, 256)[1]
            sqs.append((
                c.EPD(trg + 328 + 32 * i + 24),
                c.SetTo,
                f_mul(0x1000000, act.amount) + f_mul(0x10000, act.acttype) + act.unitid
            ))

            act.unitid = 0
            act.acttype = 0
            act.amount = 0

        # flags
        if isinstance(act.flags, EUDVariable):
            br = f_dwbreak(f_dwread_epd(c.EPD(trg + 328 + 32 * i + 28)))
            sqs.append((
                c.EPD(trg + 328 + 32 * i + 28),
                c.SetTo,
                f_mul(0x10000, br[1]) + f_mul(0x100, br[3]) + act.flags
            ))
            act.flags = 0

    if sqs:
        SeqCompute(sqs)

    c.BasicTrigger(
        conditions=conditions,
        actions=actions,
        preserved=preserved
    )
