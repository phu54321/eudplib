#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Stage 2 :
- Initialize payload (stage3+ + user code) & execute it

Since stage 2 has to be small, (stage 1's size is proportional to Stage 2's
size, and stage 1 is very big) code here don't utilize anything else than
core functionallity. (hence importing core only)
'''

from ... import core as c

import inspect


def DoActions(actions, nextptr=None):
    return c.Trigger(nextptr=nextptr, actions=actions)


def CreateStage2(payload):
    # We first build code injector.
    prtdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.prttable]))
    ortdb = c.Db(b''.join([c.i2b4(x // 4) for x in payload.orttable]))
    orig_payload = c.Db(payload.data)

    ## TABLE INITER
    if c.PushTriggerScope():
        tableiniter_start = c.NextTrigger()
        tableiniter_end = c.Forward()

        adda = c.Forward()
        loopstart = c.Forward()
        loopend = c.Forward()
        loopcond = c.Forward()

        ## BEGIN ==========

        DoActions([
            c.SetNextPtr(loopend, loopstart),  # Reset loop
        ])

        loopstart << c.NextTrigger()

        c.Trigger(
            actions=[
                c.SetMemory(adda + 16, c.SetTo, c.EPD(orig_payload)),  # Reset adder
                c.SetMemory(loopcond + 8, c.Subtract, 1),  # Loop variable
            ]
        )

        chain = [c.Forward() for _ in range(30)]

        # Read from table & write to adder action
        for i in range(29, -1, -1):
            chain[i] << c.Trigger(
                conditions=[
                    c.Memory(0, c.AtLeast, 2 ** i)  # Read from table
                ],
                actions=[
                    c.SetMemory(0, c.Subtract, 2 ** i),  # Read from table
                    c.SetMemory(adda + 16, c.Add, 2 ** i)  # Write to adder
                ]
            )

        DoActions([
            adda << c.SetMemory(0, c.Add, 0),  # Adder action
            [(
                 c.SetMemory(chain[i] + 8 + 4, c.Add, 1),  # readepd += 1
                 c.SetMemory(chain[i] + 8 + 320 + 16, c.Add, 1)  # readepd += 1
             ) for i in range(30)],
        ])

        loopend << c.Trigger(
            nextptr=0,
            conditions=[
                # Player 1's marine death should be 0 here, so we keep
                # decrementing cmpt's number until it reaches 0, when
                # it breaks out
                loopcond << c.Deaths(0, c.Exactly, 0, 0)
            ],
            actions=c.SetNextPtr(loopend, tableiniter_end)
        )

        # Loopend

        tableiniter_end << c.Trigger()
    c.PopTriggerScope()

    def QueueTable(db, addv, repn):
        dbepd = c.EPD(db)

        nexttrg = c.Forward()
        c.Trigger(
            nextptr=tableiniter_start,
            actions=[
                c.SetNextPtr(tableiniter_end, nexttrg),
                [(
                     c.SetMemory(chain[i] + 8 + 4, c.SetTo, dbepd),  # readepd += 1
                     c.SetMemory(chain[i] + 8 + 320 + 16, c.SetTo, dbepd)  # readepd += 1
                 ) for i in range(30)],
                c.SetMemory(adda + 20, c.SetTo, addv),
                c.SetMemory(loopcond + 8, c.SetTo, repn)
            ]
        )
        nexttrg << c.NextTrigger()

    ## MAIN LOGIC
    c.PushTriggerScope()
    root = c.NextTrigger()

    if payload.prttable:
        QueueTable(prtdb, orig_payload // 4, len(payload.prttable))

    # init ort
    if payload.orttable:
        QueueTable(ortdb, orig_payload, len(payload.orttable))

    # Jump
    c.Trigger(nextptr=orig_payload)

    c.PopTriggerScope()

    ####
    # return c.CreatePayload(root)
    ####

    payload = c.CreatePayload(root)
    return payload
