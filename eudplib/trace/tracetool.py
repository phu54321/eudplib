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

from .. import (
    core as c,
    utils as ut
)

import os
from . import tracecrypt


traceToolDataEPD = ut.EPD(c.Db(bytes(16 + 4 * 2048)))
recordTraceAct = c.Forward()
c.PushTriggerScope()
recordTraceTrigger = c.RawTrigger(
    actions=[
        recordTraceAct << c.SetMemoryEPD(traceToolDataEPD + 4, c.SetTo, 0)
    ]
)
c.PopTriggerScope()


def _f_initstacktrace():
    # Fill the header of trace stack with string "EUDPLIBTRACETOOL" on runtime.
    # SC:R creates a copy of STR section during EUD emulation and writes to
    # only one of the copy during emulation stage. We should read the copy
    # that is really written in-game.
    # We will fill the trace stack 'magic code' on runtime, and later find the
    # magic code to locate the stack trace table.

    c.RawTrigger(actions=[
        c.SetMemoryEPD(traceToolDataEPD + 0, c.SetTo,
                       ut.b2i4(traceHeader, 0x0)),
        c.SetMemoryEPD(traceToolDataEPD + 1, c.SetTo,
                       ut.b2i4(traceHeader, 0x4)),
        c.SetMemoryEPD(traceToolDataEPD + 2, c.SetTo,
                       ut.b2i4(traceHeader, 0x8)),
        c.SetMemoryEPD(traceToolDataEPD + 3, c.SetTo,
                       ut.b2i4(traceHeader, 0xC)),
    ])


def EUDTracePush():
    c.RawTrigger(actions=c.SetMemory(recordTraceAct + 16, c.Add, 1))


def EUDTracePop():
    EUDTraceLogRaw(0)
    c.RawTrigger(actions=c.SetMemory(recordTraceAct + 16, c.Subtract, 1))


nextTraceId = 0
traceMap = []
traceKey = 0
traceHeader = None


def _ResetTraceMap():
    """This function gets called by savemap.py::SaveMap to clear trace data."""
    global nextTraceId, traceKey, traceHeader
    nextTraceId = 0
    traceKey = ut.b2i4(os.urandom(4))
    traceMap.clear()
    traceHeader = os.urandom(16)


def EUDTraceLog(msg):
    """Log trace.

    Arguments:
        msg {str} -- Any message that you want to associate with the message.
    """

    global nextTraceId
    v = tracecrypt.mix(traceKey, nextTraceId)
    nextTraceId += 1
    if v == 0:  # We don't allow logging 0.
        v = tracecrypt.mix(traceKey, nextTraceId)
        nextTraceId += 1
    traceMap.append((v, str(msg)))

    EUDTraceLogRaw(v)


def EUDTraceLogRaw(v):
    nt = c.Forward()
    c.RawTrigger(
        nextptr=recordTraceTrigger,
        actions=[
            c.SetNextPtr(recordTraceTrigger, nt),
            c.SetMemory(recordTraceAct + 20, c.SetTo, v)
        ]
    )
    nt << c.NextTrigger()


def _GetTraceMap():
    return traceHeader, traceMap
